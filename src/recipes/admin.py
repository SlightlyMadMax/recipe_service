from django import forms
from django.contrib import admin
from durationwidget.widgets import TimeDurationWidget
from . import models


class RecipeIngredient(admin.TabularInline):
    model = models.RecipeIngredient
    autocomplete_fields = ('ingredient',)


class RecipePhotoInline(admin.StackedInline):
    model = models.RecipePhoto
    extra = 1
    max_num = 10


class BaseRecipe(admin.ModelAdmin):
    list_display_links = ('id', 'title')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["cooking_time"] = forms.DurationField(
            widget=TimeDurationWidget(
                show_days=False,
                show_hours=True,
                show_minutes=True,
                show_seconds=False
            ),
            required=True
        )
        form.base_fields["cooking_time"].label = 'Время приготовления'
        return form


@admin.register(models.SuggestedRecipe)
class SuggestedRecipe(BaseRecipe):
    list_display = ('id', 'title', 'created_at', 'author', 'is_visible')


@admin.register(models.Recipe)
class Recipe(BaseRecipe):
    list_display = ('id', 'title', 'created_at', 'has_photos', 'is_visible')
    fields = (
        'title',
        'dish',
        'category',
        'cuisine',
        'difficulty',
        'calories',
        'description',
        'instruction',
        'servings_number',
        'cooking_time',
        'is_visible'
    )
    search_fields = (
        'title',
        'dish__name',
        'description',
        'cuisine__name',
        'category__name'
    )
    autocomplete_fields = ('dish',)
    sortable_by = ('created_at', 'title', 'is_visible')
    filter_horizontal = ('cuisine',)
    list_editable = ('is_visible',)
    inlines = (RecipeIngredient, RecipePhotoInline)

    @admin.display(description='Есть фото')
    def has_photos(self, obj):
        if len(obj.photos.all()) == 0:
            return 'Нет'
        else:
            return 'Да'


@admin.register(models.Cuisine)
class Cuisine(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(models.Category)
class Category(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(models.Dish)
class Dish(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(models.Ingredient)
class Ingredient(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(models.Unit)
class Unit(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
