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
        self.assertLess(account.total, 0)

