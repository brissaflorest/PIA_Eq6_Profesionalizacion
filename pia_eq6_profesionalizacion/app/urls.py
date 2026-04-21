from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.servicio_list, name='servicio_list'), 
]