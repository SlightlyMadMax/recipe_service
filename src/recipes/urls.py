from django.urls import path
from . import views

urlpatterns = [
    path(
        'api/v1/recipe/<int:pk>/',
        views.get_by_id,
        name='recipe_by_id'
    ),
    path(
        'api/v1/recipe/random/',
        views.get_random,
        name='random_recipe'
    ),
    path(
        'api/v1/recipe/random/category/<str:cat>/',
        views.get_random_in_category,
        name='random_recipe_by_category'
    ),
    path(
        'api/v1/recipe/random/cuisine/<str:cuisine>/',
        views.get_random_by_cuisine,
        name='random_recipe_by_cuisine'
    ),
    path(
        'api/v1/recipe/filter/',
        views.get_by_parameters,
        name='recipe_by_parameters'
    ),
    path(
        'api/v1/recipe/ingredients-search/',
        views.get_by_ingredients,
        name='recipe_by_ingredients'
    ),
    path(
        'api/v1/recipe/<str:name>/',
        views.get_by_dish_name_or_title,
        name='recipe_by_name'
    )
]
