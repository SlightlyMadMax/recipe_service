from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/hints/storage-hint/<str:name>/', views.StorageHintAPI.as_view({'get': 'get_by_product_name'})),
    path('api/v1/hints/boil-hint/<str:name>/', views.BoilHintAPI.as_view({'get': 'get_by_product_name'})),
    path('api/v1/hints/substitution-hint/<str:name>/', views.SubstitutionHintAPI.as_view({'get': 'get_by_ingredient_name'}))
]
