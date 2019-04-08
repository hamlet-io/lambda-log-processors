# Lambda ALB Log Processor

This function is intended to parse log messages provided by the AWS Application Load Balancer (ALB).

The processor is fed logs through SQS based on S3 Event notifications for when a new log file is created. The processor will parse this event to find the log message location in S3, parse the event log message and send it to "sink" which is a backend that can do something with the message

## SQS Message Format

The expected message format is based on the S3 Event notifications format https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html 

An example of the payload:

```json
{
    "Records" : [
        {
            "body" : "{\"Records\":[{\"eventName\":\"ObjectCreated:Put\",\"s3\":{\"bucket\":{\"name\":\"walksregister-integration-application-stage\"},\"object\":{\"key\":\"logs/794887647097_elasticloadbalancing_ap-southeast-2_app.metering-gosource-elb-api-v1.ed00bada0007c1cb_20190325T1210Z_13.210.33.185_1b2cnuv4.log.gz\"}}}]}"
        }
    ]
}
```

## Sinks

### ElasticSearch

## Log Format

The Log format is processed based on the AWS documentation and creates one to one field mappings for each field
https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html

# index setup

```curl
PUT _template/lb_logs
{
    "template": "lb_logs*",
    "mappings": {
        "lb_log": {
            "properties": {
                "client_geoip.location": {
                    "type": "geo_point"
                },
                "request_processing_time" : {
                    "type" : "double"
                },
                "response_processing_time" : {
                    "type" : "double"
                },
                "target_processing_time" : {
                    "type" : "double"
                },
                "sent_bytes" : {
                    "type" : "integer"
                },
                "received_bytes" : {
                    "type" : "integer"
                },
                "elb_status_code" : {
                    "type" : "short"
                },
                "target_status_code" : {
                    "type" : "short"
                },
                "client_ip" : {
                    "type": "ip"
                },
                "target_ip" : {
                    "type" : "ip"
                }
            }
        }
    }
}
```