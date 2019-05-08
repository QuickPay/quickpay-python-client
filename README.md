# quickpay-python-client

[![Build Status](https://travis-ci.org/QuickPay/quickpay-python-client.svg)](https://travis-ci.org/QuickPay/quickpay-python-client)

`quickpay-python-client` is a official python client for [QuickPay API](http://tech.quickpay.net/api). Quickpay API enables you to accept payments in a secure and reliable manner. This library currently supports QuickPay `v10` api.

Installation
===============

Add to your `requirements.txt`

    quickpay-api-client

or install via [pip](https://github.com/pypa/pip):

    $ pip install quickpay-api-client

It is currently tested with Python >= `2.7.9` and Python >= `3.4`.

Usage
=====

Before doing anything you should register yourself with QuickPay and get access credentials. If you haven't please [click](http://quickpay.net) here to apply.


Create a QuickPay client
------------------------

First you should create a client instance that is anonymous or authorized with api_key or login credentials provided by QuickPay.

To initialise an anonymous client:

```
from quickpay_api_client import QPClient
client = QPClient()
```

To initialise a client with QuickPay Api Key:

```
from quickpay_api_client import QPClient
secret = ":{0}".format(os.environ['QUICKPAY_API_KEY'])
client = QPClient(secret)
```

Or you can provide login credentials like:

```
from quickpay_api_client import QPClient
secret= "{0}:{1}".format(os.environ['QUICKPAY_LOGIN'], os.environ['QUICKPAY_PASSWORD'])
client = QPClient(secret)
```

API Calls
---------

You can afterwards call any method described in QuickPay api with corresponding http method and endpoint. These methods are supported currently: `get`, `post`, `put`, `patch` and `delete`.

```
for activity in client.get('/activities'):
    print activity['id']
```

If you want raw http response, headers Please add `raw=True` parameter:

```
status, body, headers = client.get("/activities", raw=True)

if status == 200:
    for activity in json.loads(body):  ## note: import json
      print activity['id']
else:
    print "Error", body
```

Beyond the endpoint, the client accepts the following options (default values shown):

* `body: ""` ( valid for POST, PATCH and PUT)
* `headers: {}`
* `query: {}`
* `raw: false`

```python
response = client.post("/payments/1/capture",
  body={ 'amount': 100 },
  query={ "synchronized" : "" },
  raw=False
)
```

Handling API exceptions
----------------------

By default (get|post|patch|put|delete) will return JSON parsed body on success (i.e. 2xx response code) otherwise it will raise `ApiError`. Your code should handle the errors appropriately.

You can listen for any api error like:

```
from quickpay_api_client.exceptions import ApiError
try:
    client.post('/payments', currency='DKK', order_id='1212')
    ...
except ApiError as e:
    print e.body
    print e.status_code
```

You can read more about api responses at [http://tech.quickpay.net/api/](http://tech.quickpay.net/api/).
