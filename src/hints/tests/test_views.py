from rest_framework.test import APITestCase
from django.urls import reverse
from hints.models import Product, BoilHint, StorageHint, SubstitutionHint
from recipes.models import Ingredient
from utils.testing_utils.auth import get_authenticated_client


class TestViews(APITestCase):

    def setUp(self):
        self.client = get_authenticated_client()
        self.storage_hint_url = reverse('get_storage_hint', args=['product1'])
        self.boil_hint_url = reverse('get_boil_hint', args=['P1'])
        self.sub_hint_url = reverse('get_sub_hint', args=['ingredient1'])
        self.product1 = Product.objects.create(
            name='product1',
            alternative_names=['P1']
        )
        self.ingredient1 = Ingredient.objects.create(
            name='ingredient1',
            alternative_names=['i1'],
            is_default=False,
            is_allergen=False
        )

    def test_get_storage_hint_by_product_name(self):
        StorageHint.objects.create(
            product=self.product1,
            text='lalala'
        )

        response = self.client.get(self.storage_hint_url)

        self.assertEqual(response.status_code, 200)

    def test_get_boil_hint_by_product_name(self):
        BoilHint.objects.create(
            product=self.product1,
            text='lololo'
        )

        response = self.client.get(self.boil_hint_url)

        self.assertEqual(response.status_code, 200)

    def test_get_sub_hint_by_ingredient_name(self):
        SubstitutionHint.objects.create(
            ingredient=self.ingredient1,
            text='lululu'
        )

        response = self.client.get(self.sub_hint_url)

        self.assertEqual(response.status_code, 200)
