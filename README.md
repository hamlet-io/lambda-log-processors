# Lambda ALB Log Processor

This function is intended to parse log messages provided by the AWS Application Load Balancer (ALB).

The processor is fed logs through SQS based on S3 Event notifications for when a new log file is created. The processor will parse this event to find the log message location in S3, parse the event log message and send it to "sink" which is a backend that can do something with the message 

## Sinks

### ElasticSearch

## Log Format

The Log format is processed based on the AWS documentation and creates one to one field mappings for each field
https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html
