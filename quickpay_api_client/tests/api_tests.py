import base64, json
from nose.tools import assert_equal, assert_raises
import requests
from quickpay_api_client.api import QPApi
from quickpay_api_client.exceptions import ApiError
import httpretty


class TestApi(object):
    def setup(self):
        httpretty.enable()
        self.api = QPApi(secret="foo:bar")
        self.url = "{0}{1}".format(self.api.base_url, '/test')

    def setup_request(self):
        httpretty.register_uri(httpretty.GET, self.url,
                               body=json.dumps({'id': 123}),
                               content_type='application/json')

    def test_perform_success(self):
        self.setup_request()
        res = self.api.perform('get', "/test")
        assert_equal(res['id'], 123)

    def test_perform_failure(self):
        httpretty.register_uri(httpretty.GET, self.url,
                               status=500,
                               body=json.dumps({'message': 'dummy'}))

        assert_raises(ApiError, self.api.perform, 'get', '/test')

    def test_headers(self):
        self.setup_request()
        res = self.api.perform('get', '/test')

        req_headers = httpretty.last_request().headers
        assert_equal(req_headers['Authorization'], 'Basic Zm9vOmJhcg==')
        assert_equal(req_headers['Accept-Version'], 'v10')
        assert req_headers['User-Agent']

    def test_perform_when_raw(self):
        self.setup_request()
        res = self.api.perform('get', '/test', raw=True)

        assert_equal(res[0], 200)
        assert_equal(res[1], '{"id": 123}')
        assert_equal(res[2]['server'], 'Python/HTTPretty')
        assert_equal(res[2]['content-type'], 'application/json')
