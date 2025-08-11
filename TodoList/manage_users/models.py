from django.db import models

# Create your models here.
class utilisateur(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200,unique=True)
    password = models.CharField(max_length=1000)
    role = models.CharField(max_length=1000)


def __str__(self):
    return self.first_name
