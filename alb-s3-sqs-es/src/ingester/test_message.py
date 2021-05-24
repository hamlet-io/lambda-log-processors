def test_app_loadbalancer_log_http(loadbalancer_http_entry):
    msg = loadbalancer_http_entry.payload()

    assert msg['type'] == 'http'
    assert 'client_geoip' in msg


def test_app_loadbalancer_log_local_http(loadbalancer_local_http_entry):
    msg = loadbalancer_local_http_entry.payload()

    assert msg['type'] == 'http'
    assert 'client_geoip' not in msg


def test_app_loadbalancer_log_https_useragent(loadbalancer_https_entry):
    msg = loadbalancer_https_entry.payload()

    assert msg['type'] == 'https'
    assert msg['user_agent'].startswith('Mozilla/5.0 (Macintosh;')
