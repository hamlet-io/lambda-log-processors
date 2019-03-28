import os
from time import sleep
import json
import botocore
import boto3
import mylogging
from ingester.sink.elasticsearch import ElasticSink
from ingester.source import S3Source

LOGGER = mylogging.getLogger(__name__)

class Ingester:

    def __init__(
            self, sinks, bucket_name, key ):
        self.sinks = sinks
        self.bucket_name = bucket_name
        self.key = key

    def put_sinks(self, msgs):
        for sink in self.sinks:
            sink.put(msgs)

    def run(self ):
        LOGGER.debug("Fetching messages...")
        self.source = S3Source(bucket_name=self.bucket_name, key=self.key)
        msgs = self.source.get()
        LOGGER.debug(
            "Got %s message%s" % (
                len(msgs),
                '' if 1 == len(msgs) else 's'))

        self.put_sinks(msgs)

    @classmethod
    def from_environment(cls):
        sinks = []
        if 'ELASTICSEARCH_API_FQDN' in os.environ and len(os.environ.get('ELASTICSEARCH_API_FQDN')):  # NOQA
            use_sig4 = (os.environ.get("ELASTICSEARCH_API_AUTH").casefold().startswith("sig4".casefold()))  # NOQA
            elasticsearch_sink = ElasticSink(
                host=os.environ.get("ELASTICSEARCH_API_FQDN"),
                region=os.environ.get("ELASTICSEARCH_API_REGION"),
                service=os.environ.get("INGESTER_AWS_SERVICE"),
                index_name=os.environ.get("ELASTICSEARCH_API_INDEX_RAW"),
                doc_type=os.environ.get("INGESTER_ES_DOC_TYPE"),
                use_sig4=use_sig4
            )
            sinks.append(elasticsearch_sink)
        return ( sinks )

