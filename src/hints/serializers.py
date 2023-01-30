from rest_framework import serializers
from . import models


class StorageHintSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = models.StorageHint
        fields = ('name', 'text')


class BoilHintSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = models.BoilHint
        fields = ('name', 'text')


class SubstitutionHintSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )

    class Meta:
        model = models.SubstitutionHint
        fields = ('name', 'text')
