#!/usr/bin/env python

from ingester.ingester import Ingester
from __future__ import print_function

def lambda_handler(event, context):
    
    for record in event['Records']:
        for record_event in record['body']:
            print(str(record_event))
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