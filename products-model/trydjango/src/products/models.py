from django.db import models
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=False, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10_000)
    summary = models.TextField(blank=True, null=False)
    featured = models.BooleanField(default=False)  # null=True: leave empty fields in the database

    def get_absolute_url(self):
        # return f"/products/{self.id}/"
        # return reverse("product-detail", kwargs={"id": self.id})
        return reverse("products:product-detail", kwargs={"id": self.id})
        
    def __str__(self):
        return self.title