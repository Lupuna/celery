from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField(null=True)
    image_url = models.URLField()
    discount = models.IntegerField(null=True)

    def __str__(self):
        return self.name

