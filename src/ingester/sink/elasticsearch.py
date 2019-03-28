import mylogging
import json
import base64
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.exceptions import ConflictError
from ingester.sink import Sink

LOGGER = mylogging.getLogger(__name__)

def decorate(log_message):

    return log_message

class ElasticSink(Sink):

    def __init__(
        self,
        host,
        region,
        service,
        index_name,
        doc_type,
        use_sig4
    ):
        if use_sig4:
            auth = BotoAWSRequestsAuth(
                aws_host=host,
                aws_region=region,
                aws_service=service
            )
        es_args = {
            "host": host,
            "port": 443,
            "use_ssl": True
        }
        if use_sig4:
            es_args['http_auth'] = auth
            es_args['connection_class'] = RequestsHttpConnection
        self.es = Elasticsearch(**es_args)
        self.index_name = index_name
        self.doc_type = doc_type

    def _create_if_not_exists(self, index_name, body_json, doc_id):
            try:
                self.es.create(
                    index=index_name,
                    doc_type=self.doc_type,
                    body=body_json,
                    id=doc_id
                )
            except ConflictError:
                pass # Benign

    def put(self, msgs):
        for msg in msgs:

            msg_id = base64.b64encode( msg['request_creation_time'] + msg['client:port']).encode('ascii')
            data_json = json.dumps(msg)

            if msg_id and data_json and self.index_name:
                decorate(data_json)
                self._create_if_not_exists(
                    self.index_name,
                    data_json,
                    msg_id
                )