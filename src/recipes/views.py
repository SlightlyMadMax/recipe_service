from functools import reduce
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from random import choice
from . import serializers
from . import models


class SuggestRecipeAPI(CreateAPIView):
    queryset = models.SuggestedRecipe.objects.all()
    serializer_class = serializers.SuggestRecipeSerializer


def get_random_by_filter(recipe_filter):
    pks = models.Recipe.objects.filter(**recipe_filter).values_list('pk', flat=True)
    if len(pks) == 0:
        raise Http404
    random_pk = choice(pks)
    random_recipe = models.Recipe.objects.get(pk=random_pk)
    serializer = serializers.RecipeSerializer(random_recipe, many=False)
    return Response(serializer.data)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def get_by_id(request, pk=None):
    recipe = get_object_or_404(models.Recipe, pk=pk)
    serializer = serializers.RecipeSerializer(recipe, many=False)
    return Response(serializer.data)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def get_random(request):
    recipe_filter = {
        'is_visible': True,
    }
    return get_random_by_filter(recipe_filter)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def get_random_in_category(request, cat: str):
    recipe_filter = {
        'is_visible': True,
        'category__name__iexact': cat,
    }
    return get_random_by_filter(recipe_filter)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def get_random_by_cuisine(request, cuisine: str):
    recipe_filter = {
        'is_visible': True,
        'cuisine__name__iexact': cuisine,
    }
    return get_random_by_filter(recipe_filter)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def get_by_dish_name_or_title(request, name: str):
    if len(name) < 3:
        raise Http404
    recipes = models.Recipe.objects\
        .filter(Q(is_visible=True) & (Q(dish__name=name) | Q(title__icontains=name)))
    if len(recipes) == 0:
        raise Http404
    serializer = serializers.RecipeSerializer(recipes, many=True)
    return Response(serializer.data)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def get_by_parameters(request):
    params = request.query_params
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
        return get_random(request)

    recipe_filter['is_visible'] = True

    recipes = models.Recipe.objects.filter(**recipe_filter)
    if len(recipes) == 0:
        raise Http404
    serializer = serializers.RecipeSerializer(recipes, many=True)
    return Response(serializer.data)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def get_by_ingredients(request):
    names = request.query_params.getlist('ingredients')
    if len(names) < 2:
        raise Http404
    q_list = map(lambda n: Q(name__iexact=n) | Q(alternative_names__contains=[n]), names)
    q_list = reduce(lambda a, b: a | b, q_list)

    # Ищем ингредиенты по списку названий от пользователя
    names = models.Ingredient.objects\
        .filter(q_list).values_list('name', flat=True)

    if len(names) < 2:
        raise Http404

    q_list = map(lambda n: Q(ingredients__ingredient__name=n), names)
    q_list = reduce(lambda a, b: a | b, q_list)

    # Ищем рецепты, у которых есть ингредиенты из полученного списка
    # (чтобы потом несколько сузить поиск подходящих рецептов)
    recipes = models.Recipe.objects.filter(Q(is_visible=True) & q_list).distinct()

    # Получаем стандартные ингредиенты и объединяем их с полученными выше.
    # Важно, что я добавил стандартные ингредиенты только ПОСЛЕ того, как нашел рецепты по ингредиентам пользователя
    # В противном случае, возвратились бы практически все рецепты, так как, скажем, соль есть почти в любом рецепте

    default_names = models.Ingredient.objects.filter(is_default=True).values_list('name', flat=True)

    names = (names | default_names).distinct()

    # Далее, среди полученных рецептов я нахожу те, у которых список ингредиентов является подмножеством
    # ингредиентов пользователя + стандартных ингредиентов.
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
