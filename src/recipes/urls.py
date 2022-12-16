from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/recipe/<int:pk>/', views.RecipeAPI.as_view({'get': 'retrieve'})),
    path('api/v1/recipe/random/', views.RecipeAPI.as_view({'get': 'get_random'})),
    path('api/v1/recipe/random/category/<str:cat>/', views.RecipeAPI.as_view({'get': 'get_random_in_category'})),
    path('api/v1/recipe/random/cuisine/<str:cuisine>/', views.RecipeAPI.as_view({'get': 'get_random_by_cuisine'})),
    path('api/v1/recipe/filter/', views.RecipeAPI.as_view({'get': 'get_by_parameters'})),
    path('api/v1/recipe/ingredients-search/', views.RecipeAPI.as_view({'get': 'get_by_ingredients'})),
    path('api/v1/recipe/<str:name>/', views.RecipeAPI.as_view({'get': 'get_by_dish_name_or_title'}))
]
