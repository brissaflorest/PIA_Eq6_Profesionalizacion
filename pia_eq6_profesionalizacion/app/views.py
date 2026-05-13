from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Servicio, Cliente, Venta, DetalleVenta
from django.utils import timezone
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime


def generar_factura(request):
    nombre = request.GET.get('nombre', '')
    plan = request.GET.get('plan', '')
    precio = request.GET.get('precio', '0')

    # El precio que llega es el subtotal (sin IVA)
    subtotal = float(precio)
    iva = subtotal * 0.16
    total = subtotal + iva
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'

    p = canvas.Canvas(response, pagesize=letter)

    # ── Título ──────────────────────────────────────────
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(300, 780, "FACTURA")

    # ── Datos empresa ───────────────────────────────────
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 750, "Conexión Total MX")
    p.setFont("Helvetica", 11)
    p.drawString(50, 733, "Monterrey, N.L.")
    p.drawString(50, 716, "Tel: +52 81 1234 5678")
    p.drawString(50, 699, "info@conexiontotalmx.com")

    # Línea separadora
    p.line(50, 688, 550, 688)

    # ── Datos del cliente y servicio ────────────────────
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, 670, "DATOS DE LA VENTA")
    p.setFont("Helvetica", 11)
    p.drawString(50, 652, f"Fecha:    {fecha}")
    p.drawString(50, 635, f"Cliente:  {nombre}")
    p.drawString(50, 618, f"Servicio: {plan}")

    # Línea separadora
    p.line(50, 605, 550, 605)

    # ── Desglose de precios ─────────────────────────────
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50,  585, "Descripción")
    p.drawString(450, 585, "Importe")
    p.line(50, 575, 550, 575)

    p.setFont("Helvetica", 11)
    p.drawString(50,  558, plan)
    p.drawRightString(550, 558, f"${subtotal:,.2f} MXN")

    p.drawString(50,  538, "IVA (16%)")
    p.drawRightString(550, 538, f"${iva:,.2f} MXN")

    p.line(50, 526, 550, 526)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50,  508, "TOTAL")
    p.drawRightString(550, 508, f"${total:,.2f} MXN")

    # ── Pie de página ───────────────────────────────────
    p.line(50, 490, 550, 490)
    p.setFont("Helvetica", 10)
    p.drawCentredString(300, 472, "¡Gracias por su compra!")
    p.drawCentredString(300, 458, "Este documento es un comprobante de pago.")

    p.save()
    return response


def servicio_list(request):
    servicios = Servicio.objects.all()
    return render(request, 'Pia_Eq6.html', {'servicios': servicios})


def registrar_venta(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        nombre    = data.get('nombre')
        plan_nombre = data.get('plan')
        precio    = data.get('precio')

        servicio, _ = Servicio.objects.get_or_create(
            nombre=plan_nombre,
            defaults={
                'descripcion': plan_nombre,
                'precio': precio,
            }
        )

        cliente = Cliente.objects.create(nombre=nombre)

        subtotal = float(servicio.precio)
        iva      = round(subtotal * 0.16, 2)
        total    = round(subtotal + iva, 2)

        venta = Venta.objects.create(cliente=cliente, total=total)
        DetalleVenta.objects.create(venta=venta, servicio=servicio)

        fecha_local = timezone.localtime(venta.fecha)

        return JsonResponse({
            'folio':    venta.id,
            'cliente':  cliente.nombre,
            'plan':     servicio.nombre,
            'subtotal': round(subtotal, 2),
            'iva':      iva,
            'total':    total,
            'fecha':    fecha_local.strftime('%d/%m/%Y %H:%M'),
        })


def listado_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'listado_ventas.html', {'ventas': ventas})