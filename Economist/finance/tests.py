from django.test import TestCase

from .models import User, Contacts
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
