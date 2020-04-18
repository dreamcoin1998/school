from django.test import TestCase
import requests
import json


class TransactionTestCase(TestCase):

    def test_update_commody(self):
        data = {
            'name': 'Java经典',
            'description': '王小波代表作',
            'price': 10,
            'type_id': 1,
            'qq': '1285338586',
            'wx': '',
            'phone_number': '',
            'is_end': False
        }
        res = requests.post('http://127.0.0.1:8000/v1.0/transaction/transactions/', data=data)
        print(res.text)
        print(self.assertIs(res.status_code, 200))

    def test_create_images(self):
        data = {
            'imagePath': ['https://www.gaoblog.cn'],
            'commodyId': 2
        }
        res = requests.post('http://127.0.0.1:8000/v1.0/images/images/', data=data)
        print(res)
# TransactionTestCase().test_update_commody()
TransactionTestCase().test_create_images()