from __future__ import print_function
import os
from time import sleep

from ingester.sink.elasticsearch import ElasticSink
from ingester.source import S3Source

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
        print("Fetching messages...")
        self.source = S3Source(bucket_name=self.bucket_name, key=self.key)
        msgs = self.source.get(self.geoip_reader)
        print(
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
                port=int(os.environ.get('ELASTICSEARCH_API_PORT', '443')),
                use_ssl=os.environ.get('ELASTICSEARCH_API_USE_SSL', 'True'),
                region=os.environ.get("ELASTICSEARCH_API_REGION"),
                service=os.environ.get("INGESTER_AWS_SERVICE"),
                index_name=os.environ.get("ELASTICSEARCH_API_INDEX"),
                doc_type=os.environ.get("INGESTER_ES_DOC_TYPE"),
                use_sig4=use_sig4
            )
            sinks.append(elasticsearch_sink)
        return ( sinks )
