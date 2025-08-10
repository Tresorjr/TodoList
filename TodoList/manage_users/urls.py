from django.urls import include, path

from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name='main'),
    path('index', views.index, name='index'),
    path('temp/', views.temp, name='temp'),
    path('text/', views.text, name='text'),
]
 