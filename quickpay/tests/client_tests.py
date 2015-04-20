
from nose.tools import assert_equal, assert_raises
from quickpay.api import QPApi
from quickpay import QPClient
from mock import MagicMock

class TestQPClient(object):
  
  def setup(self):
    self.client = QPClient('foobar')
    self.api = self.client.api
    self.api.perform = MagicMock()
  
  def test_api_instance(self):
    assert isinstance(self.client.api, QPApi)
  
  def test_get_delegation(self):  
    self.client.get("/dummy")
    self.api.perform.assert_called_once_with("get", "/dummy")
  
  def test_post_delegation(self):  
    self.client.post("/dummy")
    self.api.perform.assert_called_once_with("post", "/dummy")
  
  def test_delete_delegation(self):  
    self.client.delete("/dummy")
    self.api.perform.assert_called_once_with("delete", "/dummy")
    
  def test_put_delegation(self):  
    self.client.put("/dummy")
    self.api.perform.assert_called_once_with("put", "/dummy")
  
  def test_patch_delegation(self):  
    self.client.patch("/dummy")
    self.api.perform.assert_called_once_with("patch", "/dummy")
  
  def test_non_http_method(self):
    assert_raises(AttributeError, self.client.foobar, "/dummy")
    
    
    
    
    