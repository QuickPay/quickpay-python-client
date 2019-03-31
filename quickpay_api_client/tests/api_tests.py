import base64
import json
from nose.tools import assert_equal, assert_raises
import requests
from quickpay_api_client.api import QPApi
from quickpay_api_client.exceptions import ApiError
import responses

class TestApi(object):
    def setup(self):
        self.api = QPApi(secret="foo:bar")
        self.url = "{0}{1}".format(self.api.base_url, '/test')

    def setup_request(self):
        responses.add(responses.GET, self.url,
                      json={'id': 123},
                      headers={"x-quickpay-server": "QP-TEST"})

    @responses.activate
    def test_perform_success(self):
        self.setup_request()
        res = self.api.perform('get', "/test")
        assert_equal(res['id'], 123)

    @responses.activate
    def test_perform_failure(self):
        responses.add(responses.GET, self.url,
                      status=500,
                      json={'message': 'dummy'})

        try:
            self.api.perform("get", "/test")
        except ApiError as err:
            assert_equal(err.body, {'message': 'dummy'})
            assert_equal(err.status_code, 500)

    @responses.activate
    def test_headers(self):
        self.setup_request()
        res = self.api.perform('get', '/test')

        req_headers = responses.calls[0].request.headers
        assert_equal(req_headers['Authorization'], 'Basic Zm9vOmJhcg==')
        assert_equal(req_headers['Accept-Version'], 'v10')
        assert req_headers['User-Agent']

    @responses.activate
    def test_callback_url_headers(self):
        self.setup_request()
        callback_url = "https://foo.bar"
        self.api.perform(
            "get", "/test", headers={'QuickPay-Callback-Url': callback_url})

        req_headers = responses.calls[0].request.headers
        assert_equal(req_headers['QuickPay-Callback-Url'], callback_url)

    @responses.activate
    def test_query_params(self):
        self.setup_request()
        self.api.perform("get", "/test", query={'foo': 'bar'})

        url = responses.calls[0].request.url
        assert(url.endswith('?foo=bar'))

    @responses.activate
    def test_post_body(self):
        responses.add(responses.POST, self.url,
                      status=200,
                      json={'message': 'dummy'})

        self.api.perform("post", "/test", query={"foo": "baz"},
                         body={'foo': 'bar'})

        last_request = responses.calls[0].request
        body = last_request.body
        parsed_body = json.loads(body)
        headers = last_request.headers

        assert_equal(parsed_body["foo"], "bar")
        assert(headers["Authorization"])
        assert(headers["Accept-Version"])
        assert(headers["User-Agent"])
        assert(last_request.url.endswith('?foo=baz'))

    @responses.activate
    def test_perform_when_raw(self):
        self.setup_request()
        res = self.api.perform('get', '/test', raw=True)

        assert_equal(res[0], 200)
        assert_equal(res[1], '{"id": 123}')
        assert_equal(res[2]['x-quickpay-server'], 'QP-TEST')
        assert_equal(res[2]['content-type'], 'application/json')
