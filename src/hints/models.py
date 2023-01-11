from django.db import models
from django.contrib.postgres.fields import ArrayField
from recipes.models import Ingredient


class Product(models.Model):
    name = models.CharField(
        max_length=127,
        null=False,
        unique=True,
        verbose_name='Название'
    )
    alternative_names = ArrayField(
        models.CharField(max_length=127),
        blank=True,
        null=True,
        verbose_name='Альтернативные названия'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class BaseHint(models.Model):
    text = models.TextField(
        null=False,
        unique=True,
        verbose_name="Текст подсказки"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.text[:50] + '...'


class BoilHint(BaseHint):
    product = models.OneToOneField(
        to=Product,
        on_delete=models.PROTECT,
        related_name='boil_hints',
        verbose_name='Продукт'
    )

    class Meta:
        verbose_name = 'Подсказка по времени варки продукта'
        verbose_name_plural = 'Подсказки по времени варки продуктов'


class StorageHint(BaseHint):
    product = models.OneToOneField(
        to=Product,
        on_delete=models.PROTECT,
        related_name='storage_hints',
        verbose_name='Продукт'
    )

    class Meta:
        verbose_name = 'Подсказка по сроку хранения продукта'
        verbose_name_plural = 'Подсказки по сроку хранения продуктов'


class SubstitutionHint(BaseHint):
    ingredient = models.OneToOneField(
        to=Ingredient,
        on_delete=models.PROTECT,
        related_name='substitution',
        verbose_name='Ингредиент'
    )

    class Meta:
        verbose_name = 'Подсказка по замене ингредиента'
        verbose_name_plural = 'Подсказки по замене ингредиентов'
