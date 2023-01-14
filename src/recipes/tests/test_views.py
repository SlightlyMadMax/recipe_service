from django.test import TestCase, Client
from django.urls import reverse
from recipes.models import *
from datetime import timedelta


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.cuisine1 = Cuisine.objects.create(
            name='кухня'
        )
        self.dish1 = Dish.objects.create(
            name='блюдо'
        )
        self.category1 = Category.objects.create(
            name='категория'
        )
        self.recipe1 = Recipe.objects.create(
            title='recipe',
            dish=self.dish1,
            category=self.category1,
            difficulty='1',
            description='123',
            instruction='321',
            calories=123,
            servings_number=3,
            cooking_time=timedelta(hours=1, minutes=30)
        )
        self.recipe1.cuisine.add(self.cuisine1)

    def test_get_random_recipe(self):
        response = self.client.get(reverse('random_recipe'))

        self.assertEquals(response.status_code, 200)

    def test_get_recipe_by_id(self):
        response = self.client.get(reverse('recipe_by_id', args=[3]))

        self.assertEquals(response.status_code, 200)

    def test_get_recipe_by_dish_name_or_title(self):
        response = self.client.get(reverse('recipe_by_name', args=['recipe']))

        self.assertEquals(response.status_code, 200)
