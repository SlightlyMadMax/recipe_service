from django.contrib import admin
from hints import models


@admin.register(models.Product)
class Product(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class BaseHint(admin.ModelAdmin):
    list_display = ('id', 'get_name', 'short_text')
    list_display_links = ('id', 'get_name')

    @admin.display(description='Текст подсказки')
    def short_text(self, obj):
        return obj.text[:50] + '...'


@admin.register(models.StorageHint)
class StorageHint(BaseHint):
    autocomplete_fields = ('product',)

    @admin.display(description='Название продукта')
    def get_name(self, obj):
        return obj.product.name


@admin.register(models.BoilHint)
class BoilHint(BaseHint):
    autocomplete_fields = ('product',)

    @admin.display(description='Название продукта')
    def get_name(self, obj):
        return obj.product.name


@admin.register(models.SubstitutionHint)
class SubstitutionHint(BaseHint):
    autocomplete_fields = ('ingredient',)

    @admin.display(description='Название ингредиента')
    def get_name(self, obj):
        return obj.ingredient.name
