from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        verbose_name="автор",
        related_name="ads",
        on_delete=models.CASCADE
    )
    price = models.IntegerField()
    description = models.CharField(max_length=3000)
    is_published = models.BooleanField(default=True)
    image = models.ImageField(upload_to="pictures", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name