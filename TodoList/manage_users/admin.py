from django.contrib import admin

# Register your models here.
from .models import membre,projet,Todo,utilisateur

admin.site.register(membre)
admin.site.register(projet)
admin.site.register(Todo)
admin.site.register(utilisateur)

