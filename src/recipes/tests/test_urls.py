from django.test import SimpleTestCase
from django.urls import reverse, resolve
from recipes.views import *


class TestUrls(SimpleTestCase):

    def test_recipe_by_id_resolves(self):
        url = reverse('recipe_by_id', args=[1])
        self.assertEqual(
            resolve(url).func,
            get_by_id
        )

    def test_random_recipe_resolves(self):
        url = reverse('random_recipe')
        self.assertEqual(
            resolve(url).func,
            get_random
        )

    def test_random_recipe_by_category_resolves(self):
        url = reverse('random_recipe_by_category', args=['Category name'])
        self.assertEqual(
            resolve(url).func,
            get_random_in_category
        )

    def test_recipe_by_cuisine_resolves(self):
        url = reverse('random_recipe_by_cuisine', args=['Cuisine name'])
        self.assertEqual(
            resolve(url).func,
            get_random_by_cuisine
        )

    def test_recipe_by_parameters_resolves(self):
        url = reverse('recipe_by_parameters')
        self.assertEqual(
            resolve(url).func,
            get_by_parameters
        )

    def test_recipe_by_ingredients_resolves(self):
        url = reverse('recipe_by_ingredients')
        self.assertEqual(
            resolve(url).func,
            get_by_ingredients
        )

    def test_recipe_by_name_resolves(self):
        url = reverse('recipe_by_name', args=['Dish name'])
        self.assertEqual(
            resolve(url).func,
            get_by_dish_name_or_title
        )
