from rest_framework import serializers
from . import models


class RecipePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecipePhoto
        fields = ('photo',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )
    unit = serializers.CharField(
        read_only=True,
        source='unit.name'
    )
    is_allergen = serializers.BooleanField(
        source='ingredient.is_allergen',
        read_only=True,
    )

    class Meta:
        model = models.RecipeIngredient
        fields = ('name', 'amount', 'unit', 'is_allergen')


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cuisine
        fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)
    photos = RecipePhotoSerializer(many=True)
    cuisine = CuisineSerializer(read_only=True, many=True)
    dish = serializers.CharField(
        source='dish.name',
        read_only=True
    )
    category = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = models.Recipe
        fields = ('title', 'cuisine', 'dish', 'category', 'difficulty', 'description', 'instruction', 'is_visible',
                  'calories', 'servings_number', 'cooking_time', 'author', 'ingredients', 'photos')


class SuggestRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SuggestedRecipe
        exclude = ('is_visible',)
