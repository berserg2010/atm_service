import pytest
from mixer.backend.django import mixer

from ..models import Banknote

pytestmark = pytest.mark.django_db


class TestBanknote:
    def test_instance(self):
        instance = mixer.blend(Banknote)
        assert instance

    def test_duplicate(self):
        banknote_1 = Banknote(
            currency='RUB',
            value=1000,
            quantity=5,
        )
        banknote_1.save()
        assert Banknote.objects.get(id=banknote_1.pk)

        banknote_2 = Banknote(
            currency='RUB',
            value=1000,
            quantity=10,
        )
        with pytest.raises(Exception):
            banknote_2.save()

    def test_update(self):
        instance = Banknote(
            currency='RUB',
            value=1000,
            quantity=5,
        )
        instance.save()

        instance.quantity = 123
        instance.save()
        assert Banknote.objects.get(pk=instance.id).quantity == 123

    def test_get_amount(self):
        assert Banknote.get_amount_currency() == 0

        instance = Banknote(
            currency='RUB',
            value=1000,
            quantity=5,
        )
        instance.save()

        assert Banknote.get_amount_currency() == 5000

        instance = Banknote(
            currency='RUB',
            value=100,
            quantity=5,
        )
        instance.save()

        assert Banknote.get_amount_currency(currency='RUB') == 5500

        instance = Banknote(
            currency='RUB',
            value=500,
            quantity=10,
        )
        instance.save()

        assert Banknote.get_amount_currency(currency='RUB', value=500) == 5000
