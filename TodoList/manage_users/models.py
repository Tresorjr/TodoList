from django.db import models
from django.utils import timezone  # meilleur pour gérer la date
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class utilisateur(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin / Chef de projet'),
        ('membre_simple', 'Membre simple'),
    ]

    first_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=1000)
    poste = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='membre_simple')

    def __str__(self):
        return f"{self.first_name} ({self.role})"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class membre(utilisateur):
    models.DateTimeField(auto_now_add=True, default=timezone.now)

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"







class projet(models.Model):
    name_project = models.CharField(max_length=200)
    description_project = models.TextField(max_length=250)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    member_project = models.ManyToManyField(membre, blank=True)

    def __str__(self):
        return self.name_project


class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=250)
    project_as = models.ForeignKey(projet, on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.ForeignKey(utilisateur, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)
    priority = models.CharField(max_length=50, default="Moyenne")  # pour gérer priorité

    def __str__(self):
        return self.title