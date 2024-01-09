import json
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

from alb_s3.ingester.ingester import Ingester

sentry_sdk.init(integrations=[AwsLambdaIntegration()], traces_sample_rate=1.0)


def lambda_handler(event, context):
    print(event)
    for record in event["Records"]:
        event_payload = json.loads(record["body"])
        for record_event in event_payload["Records"]:
            eventName = record_event["eventName"]
            if eventName.startswith("ObjectCreated:"):

                bucket_name = record_event["s3"]["bucket"]["name"]
                key = record_event["s3"]["object"]["key"]

                (sinks) = Ingester.from_environment()
                ingester = Ingester(sinks=sinks, bucket_name=bucket_name, key=key)
            ingester.run()

    return "complete"
