#!/usr/bin/env python

from ingester.ingester import Ingester

def lambda_handler(event, context):
    
    for record in event['Records']:
        eventName = record['eventName']
        if eventName.startswith('ObjectCreated:') :

            bucket_name = record["s3"]['bucket']['name']
            key = record['s3']['object']['key']

            (sinks) = Ingester.from_environment()
            ingester = Ingester(
                sinks=sinks,
                bucket_name=bucket_name,
                key=key
            )
            ingester.run()
                
    return 'complete'