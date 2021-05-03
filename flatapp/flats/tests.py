from mixer.backend.django import mixer
from django.test import TestCase
from flats.models import Flat

# Create your tests here.


class TestFlat(TestCase):

    def setUp(self):
        print('Tests flat setup')
        self.flat = mixer.blend(Flat)

    def tearDown(self):
        print('Tests flat teardown')

    def test_count_initial(self):
        self.assertEqual(self.flat.flat_count(), 1)

    def test_count(self):
        flat_new = Flat.objects.create(name='test_flat',
                                   address='Test address',
                                   electricity_t1=1,
                                   hot_water=1,
                                   cold_water=1)
        self.assertEqual(self.flat.flat_count(), 2)


