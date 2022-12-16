# Generated by Django 4.1.3 on 2022-11-21 06:47

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Кухня',
                'verbose_name_plural': 'Кухни',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('alternative_names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=127), blank=True, null=True, size=None, unique=True, verbose_name='Альтернативные названия')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('difficulty', models.CharField(choices=[('1', 'низкая'), ('2', 'средняя'), ('3', 'высокая')], default='2', max_length=1, verbose_name='Сложность')),
                ('description', models.TextField(verbose_name='Описание')),
                ('instruction', models.TextField(unique=True, verbose_name='Инструкция по приготовлению')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Показывается')),
                ('calories', models.PositiveIntegerField(verbose_name='Число ккал на 100 г.')),
                ('servings_number', models.PositiveSmallIntegerField(verbose_name='Число порций')),
                ('cooking_time', models.DurationField(verbose_name='Время приготовления')),
                ('author', models.CharField(default=None, editable=False, max_length=127, null=True, verbose_name='Автор')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipes', to='recipes.category', verbose_name='Категория')),
                ('cuisine', models.ManyToManyField(related_name='recipes', to='recipes.cuisine', verbose_name='Кухня')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipes', to='recipes.dish', verbose_name='Блюдо')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63, unique=True, verbose_name='Мера (ед. измерения)')),
            ],
            options={
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
            },
        ),
        migrations.CreateModel(
            name='RecipePhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photo/%Y/%m/%d/', verbose_name='Фото')),
                ('vk_link', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Ссылка на фото в ВК')),
                ('recipe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='photos', to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Фото рецепта',
                'verbose_name_plural': 'Фото рецепта',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recipes.ingredient', verbose_name='Название')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ingredients', to='recipes.recipe', verbose_name='Рецепт')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recipes.unit', verbose_name='Мера (ед. измерения)')),
            ],
            options={
                'verbose_name': 'Ингредиент рецепта',
                'verbose_name_plural': 'Ингредиенты рецепта',
            },
        ),
    ]
