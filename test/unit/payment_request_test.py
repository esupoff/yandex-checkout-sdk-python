import unittest
import unittest.mock

from datetime import datetime, timezone, timedelta

from yandex_checkout.domain.common.confirmation_type import ConfirmationType
from yandex_checkout.domain.common.payment_method_type import PaymentMethodType
from yandex_checkout.domain.models.airline import Airline
from yandex_checkout.domain.models.amount import Amount
from yandex_checkout.domain.models.confirmation.confirmation import Confirmation
from yandex_checkout.domain.models.confirmation.request.confirmation_redirect import ConfirmationRedirect
from yandex_checkout.domain.models.currency import Currency
from yandex_checkout.domain.models.payment_data.payment_data import PaymentData
from yandex_checkout.domain.models.payment_data.request.payment_data_webmoney import PaymentDataWebmoney
from yandex_checkout.domain.models.payment_data.request.payment_data_bank_card import PaymentDataBankCard
from yandex_checkout.domain.models.receipt import Receipt
from yandex_checkout.domain.models.recipient import Recipient
from yandex_checkout.domain.request.payment_request import PaymentRequest
import yandex_checkout.domain.request


class PaymentRequestTest(unittest.TestCase):
    def test_request_cast(self):
        self.maxDiff = None
        request = PaymentRequest()
        request.amount = Amount({'value': 0.1, 'currency': Currency.RUB})
        request.description = 'Test description'
        request.recipient = Recipient({
            'account_id': '213',
            'gateway_id': '123'
        })
        request.save_payment_method = True
        request.capture = False
        request.payment_method_data = PaymentDataWebmoney()
        request.receipt = Receipt({'phone': '79990000000', 'email': 'test@email', 'tax_system_code': 1, 'items': [
            {
                "description": "Product 1",
                "quantity": 2.0,
                "amount": {
                    "value": 250.0,
                    "currency": Currency.RUB
                },
                "vat_code": 2
            },
            {
                "description": "Product 2",
                "quantity": 1.0,
                "amount": {
                    "value": 100.0,
                    "currency": Currency.RUB
                },
                "vat_code": 2
            }
        ]})
        request.payment_method_id = '123'
        request.payment_token = '99091209012'
        request.confirmation = ConfirmationRedirect({'return_url': 'return.url'})
        request.client_ip = '192.0.0.0'
        request.metadata = {'key': 'value'}

        self.assertEqual({
            'amount': {'value': 0.1, 'currency': Currency.RUB},
            'recipient': {
                'account_id': '213',
                'gateway_id': '123'
            },
            'description': 'Test description',
            'save_payment_method': True,
            'capture': False,
            'payment_method_data': {'type': PaymentMethodType.WEBMONEY},
            'receipt': {'phone': '79990000000', 'email': 'test@email', 'tax_system_code': 1, 'items': [
                {
                    "description": "Product 1",
                    "quantity": 2.0,
                    "amount": {
                        "value": 250.0,
                        "currency": Currency.RUB
                    },
                    "vat_code": 2
                },
                {
                    "description": "Product 2",
                    "quantity": 1.0,
                    "amount": {
                        "value": 100.0,
                        "currency": Currency.RUB
                    },
                    "vat_code": 2
                }
            ]},
            'payment_method_id': '123',
            'payment_token': '99091209012',
            'confirmation': {'type': ConfirmationType.REDIRECT, 'return_url': 'return.url'},
            'client_ip': '192.0.0.0',
            'metadata': {'key': 'value'}
        }, dict(request))

    def test_request_setters(self):
        request = PaymentRequest({
            'amount': {'value': 0.1, 'currency': Currency.RUB},
            'recipient': {
                'account_id': '213',
                'gateway_id': '123'
            },
            'save_payment_method': True,
            'capture': False,
            'payment_method_data': {'type': PaymentMethodType.WEBMONEY},
            'receipt': {'phone': '79990000000', 'email': 'test@email', 'tax_system_code': 1, 'items': [
                {
                    "description": "Product 1",
                    "quantity": 2.0,
                    "amount": {
                        "value": 250.0,
                        "currency": Currency.RUB
                    },
                    "vat_code": 2
                },
                {
                    "description": "Product 2",
                    "quantity": 1.0,
                    "amount": {
                        "value": 100.0,
                        "currency": Currency.RUB
                    },
                    "vat_code": 2
                }
            ]},
            'payment_method_id': '123',
            'payment_token': '99091209012',
            'confirmation': {'type': ConfirmationType.REDIRECT, 'return_url': 'return.url'},
            'client_ip': '192.0.0.0',
            'metadata': {'key': 'value'}
        })

        self.assertIsInstance(request.confirmation, Confirmation)
        self.assertIsInstance(request.amount, Amount)
        self.assertIsInstance(request.receipt, Receipt)
        self.assertIsInstance(request.recipient, Recipient)
        self.assertIsInstance(request.payment_method_data, PaymentData)

        with self.assertRaises(TypeError):
            request.receipt = 'invalid receipt'

        with self.assertRaises(TypeError):
            request.amount = 'invalid amount'

        with self.assertRaises(TypeError):
            request.recipient = 'invalid recipient'

        with self.assertRaises(TypeError):
            request.confirmation = 'invalid confirmation'

        with self.assertRaises(TypeError):
            request.payment_method_data = 'invalid payment_method_data'

        with self.assertRaises(ValueError):
            request.payment_token = ''

    def test_request_validate(self):
        request = PaymentRequest()

        with self.assertRaises(ValueError):
            request.validate()

        request.amount = Amount({'value': 0.0, 'currency': Currency.RUB})

        with self.assertRaises(ValueError):
            request.validate()

        request.amount = Amount({'value': 0.1, 'currency': Currency.RUB})
        request.receipt = {'phone': '79990000000', 'items': [
            {
                "description": "Product 1",
                "quantity": 2.0,
                "amount": {
                    "value": 250.0,
                    "currency": Currency.RUB
                },
            },
            {
                "description": "Product 2",
                "quantity": 1.0,
                "amount": {
                    "value": 100.0,
                    "currency": Currency.RUB
                },
            }
        ]}
        with self.assertRaises(ValueError):
            request.validate()

        request.receipt = {'tax_system_code': 1, 'items': [
            {
                "description": "Product 1",
                "quantity": 2.0,
                "amount": {
                    "value": 250.0,
                    "currency": Currency.RUB
                },
                "vat_code": 2
            },
            {
                "description": "Product 2",
                "quantity": 1.0,
                "amount": {
                    "value": 100.0,
                    "currency": Currency.RUB
                },
                "vat_code": 2
            }
        ]}
        with self.assertRaises(ValueError):
            request.validate()

        request = PaymentRequest()
        request.amount = Amount({'value': 0.1, 'currency': Currency.RUB})
        request.payment_token = '123'
        request.payment_method_id = '123'
        with self.assertRaises(ValueError):
            request.validate()

        request = PaymentRequest()
        request.amount = Amount({'value': 0.1, 'currency': Currency.RUB})
        request.payment_token = '123'
        request.payment_method_data = PaymentDataWebmoney()
        with self.assertRaises(ValueError):
            request.validate()

        request = PaymentRequest()
        request.amount = Amount({'value': 0.1, 'currency': Currency.RUB})
        request.payment_method_id = '123'
        request.payment_method_data = PaymentDataWebmoney()
        with self.assertRaises(ValueError):
            request.validate()

    def test_request_validate_payment_method_id(self):
        request = PaymentRequest()
        request.amount = Amount({'value': 0.1, 'currency': Currency.RUB})
        request.payment_method_id = '2425cbf1-001f-5000-a001-181a3bf24511'

        # Should pass other validations
        request.validate()

    @unittest.mock.patch('yandex_checkout.domain.request.payment_request.datetime',
                         side_effect=datetime)
    def test_request_validate_expiry(self, modtime):
        modtime.now.return_value = datetime(year=2019, month=3, day=10)

        request = PaymentRequest()
        request.amount = Amount({'value': 0.1, 'currency': Currency.RUB})
        request.payment_method_data = PaymentDataBankCard(card={
            "number": "4111111111111111",
            "expiry_year": "2019",
            "expiry_month": "11",
            "csc": "111"
        })

        # Should pass other validations
        request.validate()

        # Obviously expired
        request.payment_method_data.card.expiry_year = '2018'
        with self.assertRaises(ValueError):
            request.validate()

        # Same month
        request.payment_method_data.card.expiry_year = '2019'
        request.payment_method_data.card.expiry_month = '03'
        request.validate()

        # Just a notch before expiration (same timezone)
        modtime.now.return_value = datetime(year=2019, month=3, day=31,
                                            hour=23, minute=59, second=59)
        request.payment_method_data.card.expiry_year = '2019'
        request.payment_method_data.card.expiry_month = '03'
        request.validate()

        # Just a notch before expiration (worst timezone case)
        client_tz = timezone(timedelta(hours=-12))
        bank_tz = timezone(timedelta(hours=+14))
        tz_offset = datetime.now(client_tz) - datetime.now(bank_tz)
        tz_offset += timedelta(hours=1)  # DST
        modtime.now.return_value += tz_offset
        request.validate()

        # Couple days after expiration
        modtime.now.return_value = datetime(year=2019, month=4, day=3)
        with self.assertRaises(ValueError):
            request.validate()
