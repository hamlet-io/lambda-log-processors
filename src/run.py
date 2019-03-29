from __future__ import print_function
from ingester.ingester import Ingester

def lambda_handler(event, context):
    print(event)
    for record in event['Records']:
        event_payload = record['body']
        for record_event in event_payload['Records']:
            eventName = record_event['eventName']
            if eventName.startswith('ObjectCreated:'):

                bucket_name = record_event["s3"]['bucket']['name']
                key = record_event['s3']['object']['key']

                (sinks) = Ingester.from_environment()
                ingester = Ingester(
                    sinks=sinks,
                    bucket_name=bucket_name,
                    key=key
                )
            ingester.run()
                
    return 'complete'