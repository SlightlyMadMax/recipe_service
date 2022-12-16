from functools import reduce
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from random import choice
from . import serializers
from . import models


class RecipeAPI(ViewSet):

    def get_queryset(self, *args, **kwargs):
        return models.Recipe.objects.filter(is_visible=True)

    def retrieve(self, pk=None, *args, **kwargs):
        recipe = get_object_or_404(models.Recipe, pk=pk)
        serializer = serializers.RecipeSerializer(recipe, many=False)
        return Response(serializer.data)

    def get_random_by_filter(self, recipe_filter):
        pks = models.Recipe.objects\
            .filter(**recipe_filter)\
            .values_list('pk', flat=True)
        if len(pks) == 0:
            raise Http404
        random_pk = choice(pks)
        random_recipe = models.Recipe.objects.get(pk=random_pk)
        serializer = serializers.RecipeSerializer(random_recipe, many=False)
        return Response(serializer.data)

    def get_random(self, *args, **kwargs):
        recipe_filter = {
            'is_visible': True,
        }
        return self.get_random_by_filter(recipe_filter)

    def get_random_in_category(self, request, cat: str):
        recipe_filter = {
            'is_visible': True,
            'category__name__iexact': cat,
        }
        return self.get_random_by_filter(recipe_filter)

    def get_random_by_cuisine(self, request, cuisine: str):
        recipe_filter = {
            'is_visible': True,
            'cuisine__name__iexact': cuisine,
        }
        return self.get_random_by_filter(recipe_filter)

    def get_by_dish_name_or_title(self, request, name: str):
        recipes = models.Recipe.objects\
            .filter(Q(is_visible=True) & (Q(dish__name=name) | Q(title__icontains=name)))
        if len(recipes) == 0:
            raise Http404
        serializer = serializers.RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def get_by_parameters(self, request):
        params = self.request.query_params
        temp_filter = {
            'cuisine__name__iexact': params.get('cuisine'),
            'category__name__iexact': params.get('category'),
            'difficulty': params.get('difficulty'),
            'calories__lte': params.get('calories'),
            'cooking_time__lte': params.get('duration')
        }
        recipe_filter = {}

        for key, value in temp_filter.items():
            if value:
                recipe_filter[key] = value

        if len(recipe_filter) == 0:
            return self.get_random()

        recipe_filter['is_visible'] = True

        recipes = models.Recipe.objects.filter(**recipe_filter)
        if len(recipes) == 0:
            raise Http404
        serializer = serializers.RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def get_by_ingredients(self, request):
        names = self.request.query_params.getlist('ingredients')
        if len(names) == 0:
            raise Http404
        q_list = map(lambda n: Q(name__iexact=n) | Q(alternative_names__contains=[n]), names)
        q_list = reduce(lambda a, b: a | b, q_list)
        names = models.Ingredient.objects\
            .filter(q_list).values_list('name', flat=True)

        q_list = map(lambda n: Q(ingredients__ingredient__name=n), names)
        q_list = reduce(lambda a, b: a | b, q_list)

        recipes = models.Recipe.objects.filter(Q(is_visible=True) & q_list).distinct()

        print(recipes)
        result = []

        for recipe in recipes.all():
            ing_names = set()
            for ri in recipe.ingredients.all():
                ing_names.add(ri.ingredient.name)
            if ing_names.issubset(names):
                result.append(recipe)

        if len(result) == 0:
            raise Http404
        serializer = serializers.RecipeSerializer(result, many=True)
        return Response(serializer.data)
