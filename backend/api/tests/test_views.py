import pytest

from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIClient
from rest_framework.utils import json

from ..models import Banknote

pytestmark = pytest.mark.django_db


class TestDeposit:
    result_data = json.dumps({
        "success": True,
    })

    @classmethod
    def setup(cls):
        cls.client = APIClient()
        cls.user = AnonymousUser()

    def test_post(self):
        data = json.dumps({
            'currency': 'RUB',
            'value': 100,
            'quantity': 10,
        })

        result = self.client.post('/deposit/', data, format='json')
        assert result.data == self.result_data

        banknote = Banknote.objects.all()
        assert banknote.count() > 0


class TestWithdraw:
    @classmethod
    def setup(cls):
        cls.client = APIClient()
        cls.user = AnonymousUser()

    def test_post(self):
        data = json.dumps({
            "currency": "RUB",
            "amount": 350,
        })

        result_data = json.dumps({
            "success": False,
        })

        result = self.client.post('/withdraw/', data, format='json')
        assert result.data == result_data

        instance = Banknote(
            currency='RUB',
            value=100,
            quantity=3,
        )
        instance.save()

        instance = Banknote(
            currency='RUB',
            value=50,
            quantity=1,
        )
        instance.save()

        result_data = json.dumps({
            "success": True,
            "result": [
                {
                    "value": 100,
                    "quantity": 3
                },
                {
                    "value": 50,
                    "quantity": 1
                }
            ]
        })
        assert Banknote.get_amount_currency() == 350
        result = self.client.post('/withdraw/', data, format='json')
        assert result.data == result_data
        assert Banknote.get_amount_currency() == 0

        data = json.dumps({
            "currency": "RUB",
            "amount": 1050,
        })

        result_data = json.dumps({
            "success": True,
            "result": [
                {
                    "value": 500,
                    "quantity": 2
                },
                {
                    "value": 50,
                    "quantity": 1
                }
            ]
        })

        instance = Banknote.objects.get(currency='RUB', value=100)
        instance.quantity = 3
        instance.save()

        instance = Banknote.objects.get(currency='RUB', value=50)
        instance.quantity = 1
        instance.save()

        instance = Banknote(
            currency='RUB',
            value=500,
            quantity=3,
        )
        instance.save()

        result = self.client.post('/withdraw/', data, format='json')
        assert result.data == result_data
