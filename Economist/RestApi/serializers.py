from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from finance.models import Charge, Account, Contacts
from .models import Token


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

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['token']