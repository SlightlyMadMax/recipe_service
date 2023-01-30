from django.contrib.postgres.fields import ArrayField
from django.db import models


class Dish(models.Model):
    name = models.CharField(
        max_length=127,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class RecipeDifficulty(models.TextChoices):
    LOW = '1', 'низкая'
    MEDIUM = '2', 'средняя'
    HIGH = '3', 'высокая'


class Cuisine(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Кухня'
        verbose_name_plural = 'Кухни'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(
        max_length=63,
        unique=True,
        verbose_name='Мера (ед. измерения)'
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название'
    )

    alternative_names = ArrayField(
        models.CharField(max_length=127),
        blank=True,
        null=True,
        verbose_name='Альтернативные названия'
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name='Стандартный ингредиент?'
    )

    is_allergen = models.BooleanField(
        default=False,
        verbose_name='Распространённый аллерген?'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return str(self.name)


class BaseRecipe(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        editable=False
    )
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название'
    )
    difficulty = models.CharField(
        max_length=1,
        choices=RecipeDifficulty.choices,
        default=RecipeDifficulty.MEDIUM,
        verbose_name='Сложность'
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name='recipes',
        verbose_name='Категория'
    )
    description = models.TextField(verbose_name='Описание')
    instruction = models.TextField(verbose_name='Инструкция по приготовлению', unique=True)
    calories = models.PositiveIntegerField(verbose_name='Число ккал на 100 г.')
    servings_number = models.PositiveSmallIntegerField(verbose_name='Число порций')
    cooking_time = models.DurationField(verbose_name='Время приготовления')
    author = models.CharField(
        verbose_name='Автор',
        null=True,
        max_length=127,
        default=None
    )

    def __str__(self):
        return self.title


class Recipe(BaseRecipe):
    cuisine = models.ManyToManyField(
        to=Cuisine,
        related_name='recipes',
        verbose_name='Кухня'
    )
    dish = models.ForeignKey(
        to=Dish,
        on_delete=models.PROTECT,
        related_name='recipes',
        verbose_name='Блюдо'
    )
    is_visible = models.BooleanField(verbose_name='Показывается', default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class SuggestedRecipe(BaseRecipe):
    cuisine = models.CharField(max_length=255, verbose_name='Кухня')
    dish = models.CharField(max_length=255, verbose_name='Блюдо')
    is_visible = models.BooleanField(verbose_name='Показывается', default=False)
    ingredients = models.JSONField(verbose_name='Ингредиенты')
    vk_photo_link = models.CharField(
        max_length=255,
        default=None,
        verbose_name='Ссылка на фото в ВК'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Предложенный рецепт'
        verbose_name_plural = 'Предложенные рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.PROTECT,
        related_name='ingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Название'
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        verbose_name='Количество'
    )
    unit = models.ForeignKey(
        to=Unit,
        on_delete=models.PROTECT,
        verbose_name='Мера (ед. измерения)'
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return str(self.ingredient.name) + ' - ' + str(self.amount) + ' ' + str(self.unit.name)


class RecipePhoto(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        related_name='photos',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Рецепт'
    )
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', verbose_name='Фото')
    vk_photo_link = models.CharField(
        null=True,
        blank=True,
        default=None,
        max_length=255,
        verbose_name='Ссылка на фото в ВК'
    )

    class Meta:
        verbose_name = 'Фото рецепта'
        verbose_name_plural = 'Фото рецепта'
