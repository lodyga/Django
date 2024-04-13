from django.db import models

class User(models.Model):
    name    = models.CharField(max_length=120),
    email   = models.CharField(max_length=120),
