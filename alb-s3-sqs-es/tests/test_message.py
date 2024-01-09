def test_app_loadbalancer_log_http(loadbalancer_http_entry):
    msg = loadbalancer_http_entry.payload()

    assert msg['type'] == 'http'
    assert 'client_geoip' in msg
    assert len(msg['client_geoip']['country_iso_code']) == 2


def test_app_loadbalancer_log_local_http(loadbalancer_local_http_entry):
    msg = loadbalancer_local_http_entry.payload()

    assert msg['type'] == 'http'
    assert 'client_geoip' not in msg


def test_app_loadbalancer_log_https_useragent(loadbalancer_https_entry):
    msg = loadbalancer_https_entry.payload()

    assert msg['type'] == 'https'
    assert msg['user_agent'].startswith('Mozilla/5.0 (Macintosh;')
    assert msg['user_agent_details']['browser'] == 'Firefox 88.0'
    assert msg['user_agent_details']['os'] == 'Mac OS X 10.15'
    assert msg['user_agent_details']['device'] == 'PC'
    assert msg['user_agent_details']['is_bot'] is False
