from django.test import TestCase
import requests


class TransactionTestCase(TestCase):

    def test_update_commody(self):
        data = {
            'name': '青铜时代',
            'description': '王小波代表作',
            'price': 10,
            'type_id': 1,
            'qq': '1285338586',
            'wx': '',
            'phone_number': '',
            'is_end': False
        }
        res = requests.put('http://127.0.0.1:8000/v1.0/transaction/transactions/1/', data=data)
        print(res.text)
        print(self.assertIs(res.status_code, 200))
TransactionTestCase().test_update_commody()