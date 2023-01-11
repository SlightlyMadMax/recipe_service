from rest_framework import serializers
from . import models


class RecipePhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField(read_only=True)

    class Meta:
        model = models.RecipePhoto
        fields = ('photo',)


class CuisineSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True, max_length=255)

    class Meta:
        model = models.Cuisine
        fields = ('name',)


class RecipeIngredientSerializer(serializers.Serializer):
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )
    amount = serializers.IntegerField(read_only=True)
    unit = serializers.CharField(
        read_only=True,
        source='unit.name'
    )

    class Meta:
        model = models.Ingredient
        fields = (
            'name',
            'amount',
            'unit',
        )


class RecipeSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    title = serializers.CharField(read_only=True, max_length=255)
    dish_name = serializers.CharField(read_only=True, source='dish.name')
    ingredients = RecipeIngredientSerializer(read_only=True, many=True)
    cuisine = CuisineSerializer(read_only=True, many=True)
    category = serializers.CharField(read_only=True, source='category.name')
    difficulty = serializers.CharField(read_only=True)
    instruction = serializers.CharField(read_only=True)
    calories = serializers.IntegerField(read_only=True, min_value=0)
    servings_number = serializers.IntegerField(read_only=True, min_value=0)
    cooking_time = serializers.DurationField(read_only=True)
    author = serializers.CharField(read_only=True, default=None)
    is_visible = serializers.BooleanField(read_only=True, default=True)
    photos = RecipePhotoSerializer(read_only=True, many=True)


class RecipeByIngredients(serializers.Serializer):
    ingredients = serializers.ListField(required=True, min_length=2)
