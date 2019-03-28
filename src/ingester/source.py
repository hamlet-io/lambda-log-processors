import botocore
import boto3
import json
import logging
from io import TextIOWrapper
from gzip import GzipFile

from ingester.message import Message
from abc import ABC

LOGGER = logging.getLogger(__name__)

class Source(ABC):

    def __init__(self):
        pass


class SQSSource(Source):

    def __init__(self, queue_name, bucket_name, batch_size=10):
        self.sqs = boto3.resource('sqs')
        self.batch_size = batch_size
        if self.sqs is None:
            # Omit sensitive data below
            raise ValueError(
                "Invalid SQS region name, access key ID or secret access key"
            )
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        if self.queue is None:
            raise ValueError("Invalid queue name '{}'".format(queue_name))
        # TODO: Set custom class for created Message instances
        # Default class is: boto.sqs.message.Message
        # self.queue.set_message_class()
        s3 = boto3.resource(
            's3',
            config=botocore.client.Config(signature_version='s3v4')
        )
        self.bucket = s3.Bucket(bucket_name)

    def get(self, poll_delay):
        sqs_msgs = self.queue.receive_messages(
            AttributeNames=['All'],
            WaitTimeSeconds=poll_delay,
            MaxNumberOfMessages=self.batch_size
        )
        msgs = []
        for sqs_msg in sqs_msgs:
            msgs.append(Message(bucket=self.bucket, sqs_msg=sqs_msg))
        return msgs

    def get_polling(self, poll_delay):
        while True:
            msgs = self.get(poll_delay)
            if len(msgs):
                break
            LOGGER.debug("No messages awaiting")
        return msgs

    def put(self, msg_body):
        return self.queue.send_message(MessageBody=msg_body)

class S3Source(Source):
    def __init__(self, bucket_name, key):
        self.s3 = boto3.resource(
            's3',
            config=botocore.client.Config(signature_version='s3v4')
        )
        self.bucket = self.s3.Bucket(bucket_name)
        self.object = self.bucket.get_key(key_name=key)
        if self.object is None:
            raise ValueError("Object Could not be found '{}'".format(key))
    
    def get(self):
        # get StreamingBody from botocore.response
        response = self.s3.get_object(Bucket=self.bucket, Key=self.object)
        # if gzipped
        gzipped = GzipFile(None, 'rb', fileobj=response['Body'])
        data = TextIOWrapper(gzipped)

        msgs = []
        for line in data:
            msgs.append(line)
        return msgs