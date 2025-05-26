from django.db import models

# Create your models here.
class Producto(models.Model):
    descripcion = models.TextField(max_length=500)
    categoria = models.CharField(max_length=50)
    fabricante = models.CharField(max_length=60)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    tiempo_entrega = models.IntegerField() # Tiempo de entrega en días
    #imagen = models.ImageField(null=True, blank=True)
    proveedor = models.CharField(max_length=60)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.descripcion}"
    
class Reporte(models.Model):
    numero_orden = models.CharField(max_length=20)
    sector = models.CharField(max_length=50)
    fecha = models.DateField()
    tipo_problema = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    def __str__(self):
        return f"{self.numero_orden}"
    
    
class Orden(models.Model):
    numero_orden = models.CharField(max_length=20)
    cliente = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_limite = models.DateField()
    sector = models.CharField(max_length=50)
    estado = models.CharField(max_length=30, default="Sin asignar")
    
    cantidad = models.IntegerField(default=1)
    producto = models.CharField(max_length=100, default="")  
    categoria = models.CharField(max_length=100, default="")   

    def __str__(self):
        return f"{self.numero_orden} - {self.cliente} - {self.estado}"
    