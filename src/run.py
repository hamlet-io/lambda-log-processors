#!/usr/bin/env python

from ingester.ingester import Ingester

def lambda_handler(event, context):
    for record in event['Records']:
        eventRecords = record['Records']
        for event in eventRecords:
            eventName = event['eventName']
            if eventName.startsWith('ObjectCreated:') :

                bucket_name = event["s3"]['bucket']['name']
                key = event['s3']['object']['key']

                (sinks) = Ingester.from_environment()
                Ingester.run(sinks=sinks bucket_name=bucket_name key=key)