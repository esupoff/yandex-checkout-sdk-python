import unittest

from yandex_checkout.domain.models.amount import Amount
from yandex_checkout.domain.models.currency import Currency
from yandex_checkout.domain.models.receipt import Receipt
from yandex_checkout.domain.models.receipt_item import ReceiptItem, PaymentSubject, PaymentMode


class ReceiptTest(unittest.TestCase):
    def test_receipt_cast(self):
        self.maxDiff = None
        receipt = Receipt()
        receipt.phone = '79990000000'
        receipt.email = 'test@email'
        receipt.tax_system_code = 1
        receipt.items = [
            {
                "description": "Product 1",
                "quantity": 2.0,
                "amount": {
                    "value": 250.0,
                    "currency": Currency.RUB
                },
                "vat_code": "2"
            },
            ReceiptItem(
                {
                    "description": "Product 2",
                    "quantity": 1.0,
                    "amount": {
                        "value": 100.0,
                        "currency": Currency.RUB
                    },
                    "vat_code": 2
                }
            )

        ]

        self.assertTrue(receipt.has_items())
        self.assertEqual({'phone': '79990000000', 'email': 'test@email', 'tax_system_code': 1, 'items': [
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
        ]}, dict(receipt))

        with self.assertRaises(TypeError):
            receipt.tax_system_code = 'invalid type'

        with self.assertRaises(ValueError):
            receipt.phone = 'invalid phone'

        with self.assertRaises(TypeError):
            receipt.items = 'invalid items'

        with self.assertRaises(TypeError):
            receipt.items = [
                'invalid item value',
                {
                    "description": "Product 2",
                    "quantity": 1.0,
                    "amount": {
                        "value": 100.0,
                        "currency": Currency.RUB
                    },
                    "vat_code": 2
                }
            ]

    def test_receipt_item(self):
        receipt_item = ReceiptItem()
        receipt_item.description = "Product"
        receipt_item.quantity = 1.0
        receipt_item.amount = Amount({
            "value": 100.0,
            "currency": Currency.RUB
        })
        receipt_item.vat_code = 2

        self.assertEqual({
            "description": "Product",
            "quantity": 1.0,
            "amount": {
                "value": 100.0,
                "currency": Currency.RUB
            },
            "vat_code": 2
        }, dict(receipt_item))

        with self.assertRaises(TypeError):
            receipt_item.amount = 'invalid amount'
