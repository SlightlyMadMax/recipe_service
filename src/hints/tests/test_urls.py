from django.test import SimpleTestCase
from django.urls import reverse, resolve
from hints.views import *


class TestUrls(SimpleTestCase):

    def test_storage_hint_by_product_name_resolves(self):
        url = reverse('get_storage_hint', args=['Product name'])
        self.assertEqual(
            resolve(url).func,
            get_storage_hint_by_product_name
        )

    def test_boil_hint_by_product_name_resolves(self):
        url = reverse('get_boil_hint', args=['Product name'])
        self.assertEqual(
            resolve(url).func,
            get_boil_hint_by_product_name
        )

    def test_sub_hint_by_ingredient_name_resolves(self):
        url = reverse('get_sub_hint', args=['Ingredient name'])
        self.assertEqual(
            resolve(url).func,
            get_sub_hint_by_ingredient_name
        )
