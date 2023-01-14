from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/hints/storage-hint/<str:name>/', views.get_storage_hint_by_product_name, name='get_storage_hint'),
    path('api/v1/hints/boil-hint/<str:name>/', views.get_boil_hint_by_product_name, name='get_boil_hint'),
    path('api/v1/hints/substitution-hint/<str:name>/', views.get_sub_hint_by_ingredient_name, name='get_sub_hint')
]
