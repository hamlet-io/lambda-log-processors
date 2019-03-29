import json
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.exceptions import ConflictError
from ingester.sink import Sink

def decorate(log_message):

    return log_message

class ElasticSink(Sink):

    def __init__(
        self,
        host,
        port,
        use_ssl,
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

        if use_ssl.casefold() == 'true' or use_ssl == '1':
            use_ssl = True
        else:
            use_ssl = False

        es_args = {
            "host": host,
            "port": port,
            "use_ssl": use_ssl
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

            id_func = getattr(msg, 'id', None)
            data_func = getattr(msg, 'payload', None)

            if id_func:
                msg_id = id_func()
            else:
                msg_id = None
            if data_func:
                data = data_func()
            else:
                data = None
            if data:
                data_json = json.dumps(data)
            else:
                data_json = None
            if msg_id and data_json and self.index_name:
                self._create_if_not_exists(
                    self.index_name,
                    data_json,
                    msg_id
                )