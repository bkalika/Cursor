import json
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from mycore.models import Room, Key
from mycore.views import KeyView
from mycore.forms import RoomForm, KeyForm, TenantForm, PersonForm, KeyTransferForm


# class KeyModelTests(TestCase):
#     def test_key_model_creation_positive_case(self):
#         room = Room(number=2)
#         room.save()
#         key = Key(room=room)
#         key.save()
#
#         keys = Key.objects.all()
#         self.assertEqual(key.room.number, 2)
#         self.assertEqual(keys[0].id, 4)

FIXTURES = ['fixtures/mycore.json']


class TestView(TestCase):
    fixtures = FIXTURES

    def test_key(self):
        response = self.client.get(reverse('key'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'key.html')

    def test_room(self):
        response = self.client.get(reverse('room'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'room.html')

    def test_person(self):
        response = self.client.get(reverse('person'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'person.html')

    def test_tenant(self):
        response = self.client.get(reverse('tenant'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tenant.html')

    def test_key_transfer(self):
        response = self.client.get(reverse('keytransfer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'key_transfer.html')


class TestViewList(TestCase):
    fixtures = FIXTURES

    def test_room_list(self):
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rooms.html')

    def test_key_list(self):
        response = self.client.get(reverse('keys'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'keys.html')

    def test_tenants_list(self):
        response = self.client.get(reverse('tenants'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tenants.html')

    def test_people_list(self):
        response = self.client.get(reverse('people'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'people.html')

    def test_keytransfers_list(self):
        response = self.client.get(reverse('keytransfers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'key_transfers.html')

    def test_tenant_detail(self):
        response = self.client.get(reverse('tenantdetail', args=['1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tenant-detail.html')


class TestForm(TestCase):
    fixtures = FIXTURES

    def test_room_form_valid(self):
        form = RoomForm(data=1)
        self.assertTrue(form.is_valid)

    def test_key_form_valid(self):
        form = KeyForm(data=1)
        self.assertTrue(form.is_valid)

    def test_person_form_valid(self):
        form = PersonForm(data='Test')
        self.assertTrue(form.is_valid)

    def test_tenant_form_valid(self):
        form = TenantForm(data={'first_name': 'AAA',
                                'last_name': 'BBB',
                                'date_of_birth': '1995-03-01',
                                'phone': '02234567'})
        self.assertTrue(form.is_valid())

    def test_key_transfer_form_valid(self):
        form = KeyTransferForm(data={'key_out_data': '2020-01-28',
                                     'room_id': '1',
                                     })
        self.assertTrue(form.is_valid)


class ApiTest(TestCase):
    fixtures = FIXTURES

    def test_api(self):
        # print(reverse('api-serializer', args=['key', '1']))
        response = self.client.get(reverse('api-serializer', args=['key', '1']), {'format': 'json'})
        # print(response)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # print(dir(response))
        self.assertEqual(json.loads(response.content.decode("utf-8")), [{"model": "mycore.key", "pk": 1, "fields": {"room": 1}}])

