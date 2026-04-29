from django.contrib import admin
from .models import Servicio, Cliente, Venta, DetalleVenta

# Register your models here.
admin.site.register(Servicio)
admin.site.register(Cliente)
admin.site.register(Venta)
admin.site.register(DetalleVenta)