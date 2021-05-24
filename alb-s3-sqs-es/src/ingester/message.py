import csv
import re
import datetime
import geoip2.errors

class Message:

    def __init__(self, log_msg, geoip_reader):

        split_log = csv.reader([ log_msg ], delimiter=' ', quotechar='"', quoting=csv.QUOTE_NONE )

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
        self.timestamp = self.message['timestamp']

        # Clean null values from message
        null_keys=[]
        for key, value in self.message.items():
            if value == '-' or value == '-1' :
                null_keys.append(key)

        for key in null_keys:
            del self.message[key]

        # Find client IP
        if self.message['client:port'] is not None:
            self.client_ip_port = self.message['client:port']

            client_ip = self.message['client:port'].split(":")
            if len(client_ip) == 2:
                self.message['client_ip'] = client_ip[0]
                self.message['client_port'] = client_ip[1]
            else:
                self.message['client_ip'] = client_ip[:-1].join(":")
                self.message['client_port'] = client_ip[-1]

        # GeoIP Lookup
        if self.message['client_ip'] is not None:
            try:
                self.geo_ip_response = geoip_reader.city(self.message['client_ip'])
            except geoip2.errors.AddressNotFoundError:
                pass # Benign

            if self.geo_ip_response is not None:

                geoip_details = {}
                if self.geo_ip_response.continent.name is not None:
                    geoip_details['continent_name'] = self.geo_ip_response.continent.name

                if self.geo_ip_response.city.name is not None:
                    geoip_details['city_name'] = self.geo_ip_response.city.name

                if self.geo_ip_response.country.name is not None:
                    geoip_details['country_name'] = self.geo_ip_response.country.name

                if self.geo_ip_response.country.iso_code is not None:
                    geoip_details['country_iso_code'] = self.geo_ip_response.country.iso_code

                if self.geo_ip_response.subdivisions.most_specific.name is not None:
                    geoip_details['region_name'] = self.geo_ip_response.subdivisions.most_specific.name

                if self.geo_ip_response.location is not None:
                    location = {
                        'lon' : self.geo_ip_response.location.longitude,
                        'lat' : self.geo_ip_response.location.latitude
                    }
                    geoip_details['location'] = location
                self.message['client_geoip'] = geoip_details

        # Expand Request details
        if self.message['request'] is not None:
            split_request = csv.reader([ self.message['request'] ], delimiter=' ', quotechar='"', quoting=csv.QUOTE_NONE )
            self.message['request_http_method'] = split_request[0]
            self.message['request_uri'] = split_request[1]
            self.message['request_http_version'] = split_request[2]

    def id(self):
        return re.sub('[^A-Za-z0-9]+', '', self.timestamp +  self.client_ip_port)

    def payload(self):
        return self.message

    def request_timestamp(self):
        return  datetime.datetime.strptime(self.timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
