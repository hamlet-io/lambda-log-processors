import shlex
import base64
import re

class Message:

    def __init__(self, log_msg):
        split_log = shlex.split(log_msg)

        self.message = {
            'type' : split_log[0],
            'timestamp' : split_log[1],
            'elb' : split_log[2],
            'client:port' : split_log[3],
            'target:port' : split_log[4],
            'request_processing_time' : split_log[5],
            'target_processing_time' : split_log[6],
            'response_processing_time' : split_log[7],
            'elb_status_code' : split_log[8],
            'target_status_code' : split_log[9],
            'received_bytes' : split_log[10],
            'sent_bytes' : split_log[11],
            'request' : split_log[12],
            'user_agent' : split_log[13],
            'ssl_cipher' : split_log[14],
            'ssl_protocol' : split_log[15],
            'target_group_arn' : split_log[16],
            'trace_id' : split_log[17],
            'domain_name' : split_log[18],
            'chosen_cert_arn' : split_log[19],
            'matched_rule_priority' : split_log[20],
            'request_creation_time' : split_log[21],
            'actions_executed' : split_log[22],
            'redirect_url' : split_log[23],
            'error_reason' : split_log[24]
        }
        self.request_creation_time = self.message['request_creation_time']
        self.request_client_ip = self.message['client:port']

    def id(self):
        return re.sub('[^A-Za-z0-9]+', '', self.request_creation_time +  self.request_client_ip)

    def payload(self):

        return self.message