# Lambda Based Log Processors

This repo contains a collection of lambda based log processors for use with AWS sourced logs

- **alb-s3-sqs-es** - Load logs from S3 into ES based on SQS S3 events
- **cloudwatch-firehose-es** - Kinesis Firehose log processor which formats logs from CloudWatch logs into messages for ElasticSearch

## Testing

To test the log processor, the serverless framework can be used with the provided sample events.

```bash
npm install
pip install -r requirements.txt
npx sls invoke local -f cloudwatch-firehose --path dev/test-event-siem-categories.json --env CATEGORIZATION_ATTRIBUTE=categories
```

To generate new events,

1. construct the desired cloud watch event structure from one of the existing `*-data.json` examples.
1. generate the expected firehose data via `gzip -c {data file} | base64
1. remove the line separators (if any) from the expected firehose data and use it to create a new firehose event based on the existing examples. It is useful to update the delivery stream name as this is shown in the trace from the function.
