from django.db import models


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True, unique=True)
    fabricante = models.CharField(max_length=100)
    descripcion = models.TextField(null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion
    
class Detalle(models.Model):
    id_detalle = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    

class Imagen(models.Model):
    id_imagen = models.AutoField(primary_key=True, unique=True)
    url = models.CharField(max_length=250)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
