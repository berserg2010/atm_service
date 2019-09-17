from rest_framework import serializers
from .models import Banknote


class BanknoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banknote
        fields = ('id', 'currency', 'value', 'quantity')
