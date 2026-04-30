from django.db import models

# Create your models here.
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    
    def __str__(self): 
        return f"{self.venta.cliente.nombre} - {self.servicio.nombre}"