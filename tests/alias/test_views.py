from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from alias.models import Alias


class TestAliasCreateView(APITestCase):
    def setUp(self):
        self.alias_data = {'target': 'https://www.example.com'}

    def test_create_alias(self):
        url = reverse('alias-create')
        response = self.client.post(url, self.alias_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Alias.objects.count(), 1)

        alias = Alias.objects.first()

        self.assertEqual(alias.target, self.alias_data['target'])
        self.assertIsNotNone(alias.alias)

    def test_create_existing_alias(self):
        existing_alias = Alias.objects.create(target='https://www.example.com', alias='ABCDEF')
        self.alias_data['target'] = existing_alias.target
        url = reverse('alias-create')
        response = self.client.post(url, self.alias_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Alias.objects.count(), 1)

        alias = Alias.objects.first()

        self.assertEqual(alias, existing_alias)

    def test_generate_unique_alias(self):
        Alias.objects.create(target='https://www.example.com/1', alias='ABCDEF')
        Alias.objects.create(target='https://www.example.com/2', alias='GHIJKL')

        url = reverse('alias-create')
        response = self.client.post(url, self.alias_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Alias.objects.count(), 3)

        alias = Alias.objects.last()

        self.assertNotEqual(alias.alias, 'ABCDEF')
        self.assertNotEqual(alias.alias, 'GHIJKL')

    def test_create_alias_missing_data(self):
        url = reverse('alias-create')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Alias.objects.count(), 0)


class TestAliasDetailView(APITestCase):
    def setUp(self):
        self.alias = Alias.objects.create(target='https://www.example.com', alias='ABCDEF')

    def test_get_alias_detail(self):
        url = reverse('alias-detail', args=[self.alias.alias])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'target': self.alias.target})

    def test_get_alias_detail_invalid_alias(self):
        url = reverse('alias-detail', args=['INVALID_ALIAS'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
