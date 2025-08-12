from django.db import models
from django.utils import timezone  # meilleur pour gérer la date
import datetime

# Create your models here.
class utilisateur(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=1000)
    role = models.CharField(max_length=1000)

    def __str__(self):
        return self.first_name


class membre(utilisateur):
    member_name = models.CharField(max_length=200)

    def __str__(self):
        return self.member_name


class projet(models.Model):
    name_project = models.CharField(max_length=200)
    description_project = models.TextField(max_length=250)
    start_date = models.DateField(default=timezone.now)  # corrigé
    end_date = models.DateField(default=timezone.now)    # corrigé
    member_project = models.ManyToManyField(membre)

    def __str__(self):
        return self.name_project


class Todo(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    project_as = models.ForeignKey(projet, on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(membre, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=timezone.now , null=True)  # corrigé

    def __str__(self):
        
        return self.title
