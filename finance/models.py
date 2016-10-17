from django.db import models

# Create your models here.


class Account(models.Model):
    _total = models.DecimalField(max_digits=15, decimal_places=2)

    @classmethod
    def create(cls, total):
        account = cls(_total = round(total, 2))
        account.save()
        return account

    def add_charge(self, value):
        if self._total + value < 0:
            return

        charge = Charge.create(self, value)
        charge.save()
        self._total += value

    def __iter__(self):
        return self.charges.all().__iter__()

    @property
    def total(self):
        return self._total


class Charge(models.Model):
    _value = models.DecimalField(max_digits=8, decimal_places=2)
    _account = models.ForeignKey('Account', related_name="charges")

    @classmethod
    def create(cls, account, value=0):
        charge = cls(_value=round(value, 2), _account=account)
        charge.save()
        return charge

    @property
    def value(self):
        return self._value



