from django.db import models


class Categoria(models.Model):
    id_categoria = models.IntegerField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id_producto = models.IntegerField(primary_key=True, unique=True)
    fabricante = models.CharField(max_length=100)
    descripcion = models.TextField(null=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column="id_categoria")

    def __str__(self):
        return self.descripcion


class Detalle(models.Model):
    id_detalle = models.IntegerField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column="id_producto")

    def __str__(self):
        return self.nombre


class Imagen(models.Model):
    id_imagen = models.IntegerField(primary_key=True, unique=True)
    URL = models.URLField()
    id_detalle = models.ForeignKey(Detalle, on_delete=models.CASCADE, db_column="id_detalle")

    def __str__(self):
        return self.id_imagen
