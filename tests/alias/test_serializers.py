from django.test import TestCase

from alias.models import Alias
from alias.serializers import AliasCreateSerializer, AliasDetailSerializer


class TestAliasCreateSerializer(TestCase):
    def setUp(self):
        self.alias_data = {'target': 'https://www.example.com'}

    def test_create_new_alias(self):
        serializer = AliasCreateSerializer(data=self.alias_data)

        self.assertTrue(serializer.is_valid())

        alias = serializer.save()

        self.assertEquals(alias.target, self.alias_data['target'])
        self.assertIsNotNone(alias.alias)

    def test_return_existing_alias(self):
        existing_alias = Alias.objects.create(target='https://www.example.com', alias='ABCDEF')
        serializer = AliasCreateSerializer(data=self.alias_data)

        self.assertTrue(serializer.is_valid())

        alias = serializer.save()

        self.assertEquals(alias, existing_alias)

    def test_generate_unique_alias(self):
        Alias.objects.create(target='https://www.example.com/1', alias='ABCDEF')
        Alias.objects.create(target='https://www.example.com/2', alias='GHIJKL')
        serializer = AliasCreateSerializer(data=self.alias_data)

        self.assertTrue(serializer.is_valid())

        alias = serializer.save()

        self.assertNotEquals(alias.alias, 'ABCDEF')
        self.assertNotEquals(alias.alias, 'GHIJKL')

    def test_to_representation(self):
        serializer = AliasCreateSerializer(data=self.alias_data)

        self.assertTrue(serializer.is_valid())

        alias = serializer.save()
        representation = serializer.to_representation(alias)

        self.assertEquals(representation['alias'], f'http://localhost:8000/{alias.alias}')


class TestAliasDetailSerializer(TestCase):
    def test_alias_detail_serializer(self):
        alias = Alias.objects.create(target='https://www.example.com', alias='ABCDEF')
        serializer = AliasDetailSerializer(alias)

        self.assertDictEqual(serializer.data, {'target': 'https://www.example.com'})
