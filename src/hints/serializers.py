from rest_framework import serializers
from . import models


class StorageHintSerializer(serializers.Serializer):
    name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    text = serializers.CharField()

    class Meta:
        model = models.StorageHint
        fields = ('name', 'text')


class BoilHintSerializer(serializers.Serializer):
    name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    text = serializers.CharField()

    class Meta:
        model = models.BoilHint
        fields = ('name', 'text')


class SubstitutionHintSerializer(serializers.Serializer):
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )
    text = serializers.CharField()

    class Meta:
        model = models.SubstitutionHint
        fields = ('name', 'text')