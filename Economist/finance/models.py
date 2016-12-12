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

    def account_statistics(self):
        accounts = self.account.all()
        acc_statistics = {}
        balance = self.balance()
        for account in accounts:
            part_of_balance = 100*account.total/balance
            part_of_balance = round(part_of_balance, 1)
            acc_statistics[account.name] = part_of_balance

        return acc_statistics

    def last_transactions(self, count):
        transactions = Charge.objects.filter(account__user = self).order_by('_date')[:count]
        return transactions


class Contacts(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='contacts')
    contacts = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='in_contacts')

    def add_contact(self, contact):
        self.contacts.add(contact)


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

    def last_transactions(self, count):
        transactions = self.charges.all().ordered_by('_date')[:count]
        return transactions

    def last_transactions_statistic(self, count=7):
        transactions = self.charges.all().ordered_by('_date')
        if not transactions:
            return []

        current_date =  transactions[0].date
        income = 0
        outcome = 0
        transactions_statistic = []
        for transaction in transactions:
            if not transaction.date == current_date:
                transactions_statistic.append({'income':income, 'outcome':outcome, 'date':current_date})
                if len(transactions_statistic) == count:
                    return transactions_statistic

                current_date = transaction.date
                income = 0
                outcome = 0

            if transaction.value > 0:
                income += transaction.value

            else:
                outcome += transaction.value

        return transactions_statistic


    def balance_statistic(self, count = 30):
        current_balance = self._total
        current_date = date.today()
        transactions = self.charges.all().ordered_by('_date')
        balance_statistic = [{'date': current_date, 'balance': current_balance}]
        if not transactions:
            return balance_statistic
        for transaction in transactions:
            if not transaction.date == current_date:
                balance_statistic.append({'date':current_date, 'balance':current_balance})
                if len(balance_statistic) ==count:
                    return balance_statistic

                current_date = transaction.date

            current_balance -= transaction.value

        return balance_statistic

    @property
    def total(self):
        return self._total

    class Meta:
        db_table = 'account'

    def __str__(self):
        return self.name + " - " + str(self.total)


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

    def __str__(self):
        return str(self.account) + " : " + str(self.value) + " " + str(self.date)