from django.urls import path
from . import views

urlpatterns = [
    path(
        'recipe/suggest/',
        views.SuggestRecipeAPI.as_view(),
        name='suggest_recipe'
    ),
    path(
        'recipe/<int:pk>/',
        views.get_by_id,
        name='recipe_by_id'
    ),
    path(
        'recipe/random/',
        views.get_random,
        name='random_recipe'
    ),
    path(
        'recipe/random/category/<str:cat>/',
        views.get_random_in_category,
        name='random_recipe_by_category'
    ),
    path(
        'recipe/random/cuisine/<str:cuisine>/',
        views.get_random_by_cuisine,
        name='random_recipe_by_cuisine'
    ),
    path(
        'recipe/filter/',
        views.get_by_parameters,
        name='recipe_by_parameters'
    ),
    path(
        'recipe/ingredients-search/',
        views.get_by_ingredients,
        name='recipe_by_ingredients'
    ),
    path(
        'recipe/<str:name>/',
        views.get_by_dish_name_or_title,
        name='recipe_by_name'
    )
]
