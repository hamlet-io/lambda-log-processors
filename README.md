# Lambda ALB Log Processor

This function is intended to parse log messages provided by the AWS Application Load Balancer (ALB).

The processor is fed logs through SQS based on S3 Event notifications for when a new log file is created. The processor will parse this event to find the log message location in S3, parse the event log message and send it to "sink" which is a backend that can do something with the message 

## SQS Message Format

The expected message format is based on the S3 Event notifications format https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html 

An example of the payload:

```json
{
    "Records": [
        {
            "eventVersion": "2.1",
            "eventSource": "aws:s3",
            "awsRegion": "ap-southeast-2",
            "eventTime": "2019-03-26T05:26:30.797Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {
                "principalId": "AWS:AROAJ76GXXA6JPXNXPHMA:Michael"
            },
            "requestParameters": {
                "sourceIPAddress": "1.1.1.1"
            },
            "responseElements": {
                "x-amz-request-id": "EFC3497BD7154E7E",
                "x-amz-id-2": "WPG6FyDkhdKUw3lGkiXg0+QAR5nlIUqeDI9/vZ9spAHZHxlNoWkYroYWS/57Zdg7Knepdt5wnT4="
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "d867b5df-3f29-40d9-a2e7-d55460f6149e",
                "bucket": {
                    "name": "walksregister-integration-application-stage",
                    "ownerIdentity": {
                        "principalId": "A3Q14ZJ3O7LD0S"
                    },
                    "arn": "arn:aws:s3:::walksregister-integration-application-stage"
                },
                "object": {
                    "key": "logs/init.sh",
                    "size": 5622,
                    "eTag": "a47d7af3bfb2658f766ff96bc3617e10",
                    "sequencer": "005C99B806C04F14A9"
                }
            }
        }
    ]
}
```

## Sinks

### ElasticSearch

## Log Format

The Log format is processed based on the AWS documentation and creates one to one field mappings for each field
https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html
