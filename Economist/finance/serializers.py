from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from .models import Charge, Account, Contacts


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = []


class ChargeSerializer(serializers.ModelSerializer):
    account = AccountSerializer

    class Meta:
        model = Charge
        fields = [
            'id',
            '_date',
            '_value'
        ]
        read_only_fields = [
            'id'
        ]


class StatsByMonthSerializer(serializers.ModelSerializer):
    month = serializers.CharField(max_length=16)
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
