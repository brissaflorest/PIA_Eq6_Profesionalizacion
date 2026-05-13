from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.servicio_list, name='inicio'),
    path('registrar-venta/', views.registrar_venta, name='registrar_venta'),
    path('listado_ventas/', views.listado_ventas, name='listado_ventas'),
    path('generar-factura/', views.generar_factura, name='generar_factura'),
]