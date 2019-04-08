import botocore
import boto3
import json
from io import TextIOWrapper
from gzip import GzipFile
from ingester.message import Message
from abc import ABC

class Source(ABC):

    def __init__(self):
        pass

class S3Source(Source):
    def __init__(self, bucket_name, key):
        self.s3 = boto3.resource(
            's3',
            config=botocore.client.Config(signature_version='s3v4')
        )
        self.bucket = self.s3.Bucket(bucket_name)
        self.object = self.s3.Object(bucket_name=bucket_name, key=key)
        if self.object is None:
            raise ValueError("Object Could not be found '{}'".format(key))
    
    def get(self):
        # get StreamingBody from botocore.response
        response = self.object.get()

        try: 
            gzipped = GzipFile(None, 'rb', fileobj=response['Body'])
            data = TextIOWrapper(gzipped)
        except OSError:
            return []

        msgs = []
        for line in data:
            msgs.append(Message(line))
        return msgs