import datetime
from django.test import TestCase

from .models import User, Contacts, Charge, Account
# Create your tests here.

class ContactsTest(TestCase):

    def test_many_times_adding_contact(self):
        user1 = User.objects.create_user(username='user1', password='user1', email='user1@test.ru')
        user2 = User.objects.create_user(username='user2', password='user2', email='user2@test.ru')
        contacts_list = Contacts()
        contacts_list.owner = user1
        contacts_list.save()
        contacts_list.add_contact(user2)
        self.assertEqual(len(contacts_list.contacts.all()), 1)
        contacts_list.add_contact(user2)
        self.assertEqual(len(contacts_list.contacts.all()), 1)

class AccountTest(TestCase):

    def test_negative_balance(self):
        user = User.objects.create_user(username='user', password='user', email='user@test.ru')
        account = Account.create(100, 'test_account1', user)
        charge = Charge.create(-1000)
        account.add_charge(charge)
        self.assertEqual(100, account.total)

    def test_last_transactions_statistic(self):
        user = User.objects.create_user(username='user', password='user', email='user@test.ru')
        account = Account.create(100, 'test_account_stat', user)

        for i in range(1, 16):
            charge = Charge.create(100+i, datetime.date(2016, 12, i))
            account.add_charge(charge)
        charge = Charge.create(-500, datetime.date.today())
        account.add_charge(charge)
        test_statistics = [{'income': 109, 'outcome': 0, 'date': datetime.date(2016, 12, 9)},
                           {'income': 110, 'outcome': 0, 'date': datetime.date(2016, 12, 10)},
                           {'income': 111, 'outcome': 0, 'date': datetime.date(2016, 12, 11)},
                           {'income': 112, 'outcome': 0, 'date': datetime.date(2016, 12, 12)},
                           {'income': 113, 'outcome': 0, 'date': datetime.date(2016, 12, 13)},
                           {'income': 114, 'outcome': 0, 'date': datetime.date(2016, 12, 14)},
                           {'income': 115, 'outcome': -500, 'date': datetime.date(2016, 12, 15)}]
        test_statistics.reverse()
        transactions_statistic = account.last_transactions_statistic()
        for stat in transactions_statistic:
            print(stat)
        for i in range(len(transactions_statistic)):
            self.assertEqual(transactions_statistic[i], test_statistics[i])