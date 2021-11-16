"""
For processing data sent to Firehose by Cloudwatch Logs subscription filters.

Cloudwatch Logs sends to Firehose records that look like this:

{
  "messageType": "DATA_MESSAGE",
  "owner": "123456789012",
  "logGroup": "log_group_name",
  "logStream": "log_stream_name",
  "subscriptionFilters": [
    "subscription_filter_name"
  ],
  "logEvents": [
    {
      "id": "01234567890123456789012345678901234567890123456789012345",
      "timestamp": 1510109208016,
      "message": "log message 1"
    },
    {
      "id": "01234567890123456789012345678901234567890123456789012345",
      "timestamp": 1510109208017,
      "message": "log message 2"
    }
    ...
  ]
}

The data is additionally compressed with GZIP.

The code below will:

1) Gunzip the data
2) Parse the json
3) Set the result to ProcessingFailed for any record whose messageType is not DATA_MESSAGE, thus redirecting them to the
   processing error output. Such records do not contain any log events. You can modify the code to set the result to
   Dropped instead to get rid of these records completely.
4) For records whose messageType is DATA_MESSAGE, extract the individual log events from the logEvents field, and pass
   each one to the transformLogEvent method. You can modify the transformLogEvent method to perform custom
   transformations on the log events.
5) Concatenate the result from (4) together and set the result as the data of the record returned to Firehose. Note that
   this step will not add any delimiters. Delimiters should be appended by the logic within the transformLogEvent
   method.
6) Any additional records which exceed 6MB will be re-ingested back into Firehose.

"""

from io import BytesIO
import base64
import json
import gzip
import boto3
import datetime


def transformLogEvent(log_event, cloudwatch_info):
    """Transform each log event.

    The default implementation below will to to create a json message from the message field if it can't
    the message will be passed as a string. This should allow support for JSON and string cloudwatch logs

    Args:
    log_event (dict): The original log event. Structure is {"id": str, "timestamp": long, "message": str}

    Returns:
    str: The transformed log event.
    """

    json_event = {}

    isotime = datetime.datetime.utcfromtimestamp( log_event['timestamp'] / 1000 ).isoformat()

    try:
        json_event = json.loads(log_event['message'])
        if json_event.get('timestamp') is None:
            json_event['timestamp'] = isotime

    except json.JSONDecodeError:
        json_event = {
            'message' : log_event['message'],
            'timestamp' : isotime
        }

    json_event['cloudwatch'] = cloudwatch_info

    return json.dumps(json_event)

def processRecords(records):
    for r in records:
        data = base64.b64decode(r['data'])
        with gzip.open(BytesIO(data), 'rb') as f:
            data = json.loads(f.read())

        recId = r['recordId']
        """
        CONTROL_MESSAGE are sent by CWL to check if the subscription is reachable.
        They do not contain actual data.
        """
        if data['messageType'] == 'CONTROL_MESSAGE':
            yield {
                'result': 'Dropped',
                'recordId': recId
            }
        elif data['messageType'] == 'DATA_MESSAGE':

            cloudwatch_info = {}
            cloudwatch_info['log_group'] = data['logGroup']
            cloudwatch_info['log_stream'] = data['logStream']

            for i, event in enumerate(data['logEvents']):
                if i == 0:
                    cw_log_data = transformLogEvent(event, cloudwatch_info)

                    # Determine if extra ways to categorize the event were provided
                    categories = getattr(cw_log_data, 'categories', [] )
                    if not isinstance(categories, list):
                        categories = [categories]

                    # Get unique categories - ensure Logs is always in the list at a minimum
                    categories = list(set(categories.append('Logs')))

                    for j,category in enumerate(categories):
                        if j == 0:
                            cw_log_data['categories'] = category

                            yield {
                                'data' : str(base64.b64encode(cw_log_data.encode()), 'utf-8'),
                                'result' : 'Ok',
                                'recordId' : recId,
                                'metadata' : {
                                    'partitionKeys': {
                                        'category' : category
                                    }
                                }
                            }

                        else:
                            category_event = event
                            category_event['categories'] = [category]

                            reingest_event = data
                            reingest_event['logEvents'] = [ category_event ]

                            reingest_json = json.dumps(reingest_event)
                            reingest_bytes = reingest_json.encode('utf-8')
                            reignest_compress = gzip.compress(reingest_bytes)

                            yield {
                                'data' : str( base64.b64encode( reignest_compress ), 'utf-8'),
                                'result' : 'Reingest',
                                'recordId' : recId
                            }

                else:

                    reingest_event = data
                    reingest_event['logEvents'] = [ event ]

                    reingest_json = json.dumps(reingest_event)
                    reingest_bytes = reingest_json.encode('utf-8')
                    reignest_compress = gzip.compress(reingest_bytes)

                    yield {
                        'data' : str( base64.b64encode( reignest_compress ), 'utf-8'),
                        'result' : 'Reingest',
                        'recordId' : recId
                    }
        else:
            yield {
                'result': 'Dropped',
                'recordId': recId
            }

def putRecordsToFirehoseStream(streamName, records, client, attemptsMade, maxAttempts):
    failedRecords = []
    codes = []
    errMsg = ''
    # if put_record_batch throws for whatever reason, response['xx'] will error out, adding a check for a valid
    # response will prevent this
    response = None
    try:
        response = client.put_record_batch(DeliveryStreamName=streamName, Records=records)
    except Exception as e:
        failedRecords = records
        errMsg = str(e)

    # if there are no failedRecords (put_record_batch succeeded), iterate over the response to gather results
    if not failedRecords and response and response['FailedPutCount'] > 0:
        for idx, res in enumerate(response['RequestResponses']):
            # (if the result does not have a key 'ErrorCode' OR if it does and is empty) => we do not need to re-ingest
            if 'ErrorCode' not in res or not res['ErrorCode']:
                continue

            codes.append(res['ErrorCode'])
            failedRecords.append(records[idx])

        errMsg = 'Individual error codes: ' + ','.join(codes)

    if len(failedRecords) > 0:
        if attemptsMade + 1 < maxAttempts:
            print('Some records failed while calling PutRecordBatch to Firehose stream, retrying. %s' % (errMsg))
            putRecordsToFirehoseStream(streamName, failedRecords, client, attemptsMade + 1, maxAttempts)
        else:
            raise RuntimeError('Could not put records after %s attempts. %s' % (str(maxAttempts), errMsg))

def createReingestionRecord(originalRecord):
    return {'data': base64.b64decode(originalRecord['data'])}

def getReingestionRecord(reIngestionRecord):
    return {'Data': reIngestionRecord['data']}

def lambda_handler(event, context):
    streamARN = event['deliveryStreamArn']
    region = streamARN.split(':')[3]
    streamName = streamARN.split('/')[1]

    print('Stream: %s, Region: %s, Received: %d' % (streamName, region, len(event['records'])) )

    records = list(processRecords(event['records']))
    print('Expanded Total: %d' % (len(records)) )

    projectedSize = 0
    dataByRecordId = {rec['recordId']: createReingestionRecord(rec) for rec in event['records']}
    putRecordBatches = []
    recordsToReingest = []
    totalRecordsToBeReingested = 0
    recordsToReturn = []

    for idx, rec in enumerate(records):
        if rec['result'] != 'Ok' and rec['result'] != 'Reingest':
            continue

        projectedSize += len(rec['data']) + len(rec['recordId'])
        # 6000000 instead of 6291456 to leave ample headroom for the stuff we didn't account for
        if projectedSize > 6000000 or rec['result'] == 'Reingest':
            totalRecordsToBeReingested += 1

            if rec['result'] == 'Reingest':
                recordsToReingest.append(
                    getReingestionRecord(createReingestionRecord(rec))
                )
            else:
                recordsToReingest.append(
                    getReingestionRecord(dataByRecordId[rec['recordId']])
                )
                records[idx]['result'] = 'Dropped'
                del(records[idx]['data'])

        if rec['result'] != 'Reingest':
                recordsToReturn.append(rec)

        # split out the record batches into multiple groups, 500 records at max per group
        if len(recordsToReingest) == 500:
            putRecordBatches.append(recordsToReingest)
            recordsToReingest = []

    if len(recordsToReingest) > 0:
        # add the last batch
        putRecordBatches.append(recordsToReingest)

    # iterate and call putRecordBatch for each group
    recordsReingestedSoFar = 0
    if len(putRecordBatches) > 0:
        print('Total reingestion batches: %d' % (len(putRecordBatches)) )
        client = boto3.client('firehose', region_name=region)
        for recordBatch in putRecordBatches:
            putRecordsToFirehoseStream(streamName, recordBatch, client, attemptsMade=0, maxAttempts=20)
            recordsReingestedSoFar += len(recordBatch)
            print('Reingested %d/%d' % (recordsReingestedSoFar, totalRecordsToBeReingested ))
    else:
        print('No records to be reingested')

    print( 'Records processed: ' + str(len(recordsToReturn)) + ' - Log records found: ' + str(len(records)) )

    return {"records": recordsToReturn}
