from django.shortcuts import render
from django.http import JsonResponse
from .models import Servicio, Cliente, Venta, DetalleVenta
import json

def servicio_list(request):
    servicios = Servicio.objects.all()
    return render(request, 'Pia_Eq6.html', {'servicios': servicios})

def registrar_venta(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        plan_nombre = data.get('plan')
        precio = data.get('precio')

        # Buscar o crear el servicio
        servicio, _ = Servicio.objects.get_or_create(
            nombre=plan_nombre,
            defaults={'descripcion': plan_nombre, 'precio': precio}
        )

        # Crear cliente y venta
        cliente = Cliente.objects.create(nombre=nombre)
        venta = Venta.objects.create(cliente=cliente, total=servicio.precio)
        DetalleVenta.objects.create(venta=venta, servicio=servicio)

        return JsonResponse({
            'folio': venta.id,
            'cliente': cliente.nombre,
            'plan': servicio.nombre,
            'total': str(venta.total),
            'fecha': venta.fecha.strftime('%d/%m/%Y %H:%M'),
        })
# Create your views here.
def servicio_list(request):
    servicios = Servicio.objects.all()
    return render(request, 'Pia_Eq6.html', {'servicios': servicios})

def registrar_venta(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        plan_nombre = data.get('plan')
        precio = data.get('precio')

        # Buscar o crear el servicio
        servicio, _ = Servicio.objects.get_or_create(
            nombre=plan_nombre,
            defaults={'descripcion': plan_nombre, 'precio': precio}
        )

        # Crear cliente y venta
        cliente = Cliente.objects.create(nombre=nombre)
        venta = Venta.objects.create(cliente=cliente, total=servicio.precio)
        DetalleVenta.objects.create(venta=venta, servicio=servicio)

        return JsonResponse({
            'folio': venta.id,
            'cliente': cliente.nombre,
            'plan': servicio.nombre,
            'total': str(venta.total),
            'fecha': venta.fecha.strftime('%d/%m/%Y %H:%M'),
        })