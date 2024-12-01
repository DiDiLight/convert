import urllib.parse

from django.urls import reverse
from rest_framework.test import APITestCase

def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' +   urllib.parse.urlencode(get)
    return url

class ApiTestClass(APITestCase):
    def setUp(self):
        pass

    def test_ok(self):
        url = build_url('rates', get={'from': 'USD', 'to': 'EUR', 'value': '10'})
        response = self.client.get(url, format='json')
        self.assertEqual(200, response.status_code)

    def test_false(self):
        url = build_url('rates', get={'from': 'USD', 'to': 'EUR'})
        response = self.client.get(url, format='json')
        self.assertEqual(400, response.status_code)
        url = build_url('rates', get={'from': 'USDddddd', 'to': 'EUR', 'value': '10'})
        response = self.client.get(url, format='json')
        self.assertEqual(400, response.status_code)

