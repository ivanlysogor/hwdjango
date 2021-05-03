from django.test import TestCase
from .models import Flat
from django.contrib.contenttypes.models import ContentType


class TestFlatListView(TestCase):

    def setUp(self):
        print('Tests flat list view setup')

    def tearDown(self):
        print('Tests flat list view teardown')

    def test_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_content(self):
        # client = Client()
        response = self.client.get('/')
        # print(response.content)
        self.assertIn('Add a flat', response.content.decode(encoding='utf-8'))


class TestFlatUpdateView(TestCase):

    def setUp(self):
        print('Tests flat update view setup')
        self.id = Flat.objects.create(name='test_flat',
                                      address='Test address',
                                      electricity_t1=1,
                                      hot_water=1, cold_water=1).id


    def tearDown(self):
        print('Tests flat update view teardown')

    def test_update(self):
        response = self.client.get(f'/update/{self.id}/')
        self.assertEqual(response.status_code, 200)

