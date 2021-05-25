import pytest

from ingester.message import Message

@pytest.fixture
def loadbalancer_local_http_entry():
    return Message(
        '''http 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 192.168.131.39:2817 10.0.0.1:80 0.000 0.001 0.000 200 200 34 366 "GET http://www.example.com:80/?a=b&c=d&zip=98101 HTTP/1.1" "curl/7.46.0" - - arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337262-36d228ad5d99923122bbe354" "-" "-" 0 2018-07-02T22:22:48.364000Z "forward" "-" "-"'''
    )  # noqa: E501

@pytest.fixture
def loadbalancer_http_entry():
    return Message(
        '''http 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 1.2.3.4:2817 10.0.0.1:80 0.000 0.001 0.000 200 200 34 366 "GET http://www.example.com:80/?a=b&c=d&zip=98101 HTTP/1.1" "curl/7.46.0" - - arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337262-36d228ad5d99923122bbe354" "-" "-" 0 2018-07-02T22:22:48.364000Z "forward" "-" "-"'''
    )  # noqa: E501


@pytest.fixture
def loadbalancer_https_entry():
    return Message(
        '''https 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 1.2.3.4:2817 10.0.0.1:80 0.086 0.048 0.037 200 200 0 57 "GET https://www.example.com:443/ HTTP/1.1" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0" ECDHE-RSA-AES128-GCM-SHA256 TLSv1.2 arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337281-1d84f3d73c47ec4e58577259" "www.example.com" "arn:aws:acm:us-east-2:123456789012:certificate/12345678-1234-1234-1234-123456789012" 1 2018-07-02T22:22:48.364000Z "authenticate,forward" "-" "-"'''
    )  # noqa: E501


@pytest.fixture
def loadbalancer_http2_entry():
    return Message(
        '''h2 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 1.2.3.4:48160 10.0.0.66:9000 0.000 0.002 0.000 200 200 5 257 "GET https://10.0.2.105:773/ HTTP/2.0" "curl/7.46.0" ECDHE-RSA-AES128-GCM-SHA256 TLSv1.2 arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337327-72bd00b0343d75b906739c42" "-" "-" 1 2018-07-02T22:22:48.364000Z "redirect" "https://example.com:80/" "-"'''
    )  # noqa: E501


@pytest.fixture
def loadbalancer_websockets_entry():
    return Message(
        '''ws 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 1.2.3.4:40914 10.0.1.192:8010 0.001 0.003 0.000 101 101 218 587 "GET http://10.0.0.30:80/ HTTP/1.1" "-" - - arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337364-23a8c76965a2ef7629b185e3" "-" "-" 1 2018-07-02T22:22:48.364000Z "forward" "-" "-"'''
    )  # noqa: E501


@pytest.fixture
def loadbalancer_secured_websockets_entry():
    return Message(
        '''wss 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 1.2.3.4:44244 10.0.0.171:8010 0.000 0.001 0.000 101 101 218 786 "GET https://10.0.0.30:443/ HTTP/1.1" "-" ECDHE-RSA-AES128-GCM-SHA256 TLSv1.2 arn:aws:elasticloadbalancing:us-west-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337364-23a8c76965a2ef7629b185e3" "-" "-" 1 2018-07-02T22:22:48.364000Z "forward" "-" "-"'''
    )  # noqa: E501


@pytest.fixture
def loadbalancer_lambda_entry():
    return Message(
        '''http 2018-11-30T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 1.2.3.4:2817 - 0.000 0.001 0.000 200 200 34 366 "GET http://www.example.com:80/ HTTP/1.1" "curl/7.46.0" - - arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337364-23a8c76965a2ef7629b185e3" "-" "-" 0 2018-11-30T22:22:48.364000Z "forward" "-" "-"'''
    )  # noqa: E501


@pytest.fixture
def loadbalancer_lambda_failed_entry():
    return Message(
        '''http 2018-11-30T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 1.2.3.4:2817 - 0.000 0.001 0.000 502 - 34 366 "GET http://www.example.com:80/ HTTP/1.1" "curl/7.46.0" - - arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337364-23a8c76965a2ef7629b185e3" "-" "-" 0 2018-11-30T22:22:48.364000Z "forward" "-" "LambdaInvalidResponse"'''
    )  # noqa: E501


@pytest.fixture
def loadbalancer_cloudfront_forward():
    return Message(
        '''http 2018-11-30T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 1.2.3.4:2817 - 0.000 0.001 0.000 502 - 34 366 "GET http://www.example.com:80/ HTTP/1.1" "curl/7.46.0" - - arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337364-23a8c76965a2ef7629b185e3" "-" "-" 0 2018-11-30T22:22:48.364000Z "waf,forward" "-" "-"'''
    )  # noqa: E501


@pytest.fixture
def loadbalancer_cloudfront_forward_refused():
    return Message(
        '''http 2018-11-30T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 1.2.3.4:2817 - 0.000 0.001 0.000 502 - 34 366 "GET http://www.example.com:80/ HTTP/1.1" "curl/7.46.0" - - arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337364-23a8c76965a2ef7629b185e3" "api.example.com" "session-reused" 0 2018-11-30T22:22:48.364000Z "waf,forward" "-" "-"'''
    )  # noqa: E501


@pytest.fixture
def loadbalancer_cloudfront_forward_h2():
    return Message(
        '''h2 2018-11-30T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 1.2.3.4:2817 - 0.000 0.001 0.000 502 - 34 366 "GET http://www.example.com:80/ HTTP/1.1" "curl/7.46.0" - - arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337364-23a8c76965a2ef7629b185e3" "api.example.com" "-" 0 2018-11-30T22:22:48.364000Z "waf,forward" "-" "-"'''
    )  # noqa: E501
