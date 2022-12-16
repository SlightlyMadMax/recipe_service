from django.db import models
from django.contrib.postgres.fields import ArrayField
from recipes.models import Ingredient


class Product(models.Model):
    name = models.CharField()
    alternative_names = ArrayField(
        models.CharField(max_length=127),
        unique=True,
        blank=True,
        null=True,
        verbose_name='Альтернативные названия'
    )


class Hint(models.Model):
    hint_text = models.TextField(
        null=False,
        unique=True,
        verbose_name="Текст подсказки"
    )

    class Meta:
        abstract = True


class BoilHint(Hint):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.PROTECT,
        related_name='hints',
        verbose_name='Продукт'
    )

    class Meta:
        verbose_name = 'Подсказка по времени варки продукта'
        verbose_name_plural = 'Подсказки по времени варки продуктов'


class StorageHint(Hint):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.PROTECT,
        related_name='hints',
        verbose_name='Продукт'
    )

    class Meta:
        verbose_name = 'Подсказка по сроку хранения продукта'
        verbose_name_plural = 'Подсказки по сроку хранения продуктов'


class SubstitutionHint(Hint):
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.PROTECT,
        related_name='substitution',
        verbose_name='Ингредиент'
    )

    class Meta:
        verbose_name = 'Подсказка по замене ингредиента'
        verbose_name_plural = 'Подсказки по замене ингредиентов'
