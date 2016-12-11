from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=16)
    address = models.CharField(max_length=50)

    def balance(self):
        balance = 0
        accounts = self.account.all()
        for account in accounts:
            balance += account.total

        return balance


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='account')
    _total = models.DecimalField(max_digits=15, decimal_places=2)
    name = models.CharField(max_length=20)
    @classmethod
    def create(cls, total):
        account = cls(_total = round(total, 2))
        account.save()
        return account

    def add_charge(self, charge):
        if self._total + charge.value < 0:
            return

        charge.account = self
        charge.save()
        self._total += charge.value
        self.save()

    def __iter__(self):
        return self.charges.all().__iter__()

    @property
    def total(self):
        return self._total

    class Meta:
        db_table = 'account'


class Charge(models.Model):
    _value = models.DecimalField(max_digits=8, decimal_places=2)
    _date = models.DateField()
    account = models.ForeignKey("Account", related_name="charges")

    @classmethod
    def create(cls, account, Value=0, Date = date.today()):
        charge = cls(_value=round(Value, 2), _date = Date, account=account)
        charge.save()
        return charge

    @property
    def value(self):
        return self._value

    @property
    def date(self):
        return self._date