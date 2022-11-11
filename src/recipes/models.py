from django.db import models


class Dish(models.Model):
    title = models.CharField(max_length=127)


class Cuisine(models.Model):
    pass


class Recipe(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created_at']


class Ingredient(models.Model):
    pass


class Substitute(models.Model):
    pass


class BoilingHint(models.Model):
    pass


class StorageHint(models.Model):
    pass
