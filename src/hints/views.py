from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from . import models
from . import serializers


@api_view(('GET',))
def get_storage_hint_by_product_name(request, name: str):
    hint = get_object_or_404(
        models.StorageHint,
        Q(product__name__iexact=name) | Q(product__alternative_names__contains=[name])
    )
    serializer = serializers.StorageHintSerializer(hint, many=False)
    return Response(serializer.data)


@api_view(('GET',))
def get_boil_hint_by_product_name(request, name: str):
    hint = get_object_or_404(
        models.BoilHint,
        Q(product__name__iexact=name) | Q(product__alternative_names__contains=[name])
    )
    serializer = serializers.BoilHintSerializer(hint, many=False)
    return Response(serializer.data)


@api_view(('GET',))
def get_sub_hint_by_ingredient_name(request, name: str):
    hint = get_object_or_404(
        models.SubstitutionHint,
        Q(ingredient__name__iexact=name) | Q(ingredient__alternative_names__contains=[name])
    )
    serializer = serializers.SubstitutionHintSerializer(hint, many=False)
    return Response(serializer.data)
