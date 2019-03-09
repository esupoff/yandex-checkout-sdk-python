import unittest
from unittest.mock import patch

from yandex_checkout.client import ApiClient
from yandex_checkout.configuration import Configuration
from yandex_checkout.domain.common.http_verb import HttpVerb
from yandex_checkout.domain.common.request_object import RequestObject


@unittest.skip("Not implemented properly")
class ClientTest(unittest.TestCase):
    def setUp(self):
        Configuration.configure(account_id='test_account_id', secret_key='test_secret_key')

    def test_request(self):
        client = ApiClient()
        with patch('request.Session.request') as request_mock:
            request_mock.return_value = {
                'amount': {'currency': 'RUB', 'value': 1.0},
                'created_at': '2017-11-30T15:45:31.130Z',
                'id': '21b23b5b-000f-5061-a000-0674e49a8c10',
                'metadata': {'float_value': '123.32', 'key': 'data'},
                'paid': False,
                'payment_method': {'type': 'bank_card'},
                'recipient': {'account_id': '156833', 'gateway_id': '468284'},
                'status': 'canceled'
            }

            client.request(HttpVerb.POST, '/path', RequestObject(), {'header': 'header'})
