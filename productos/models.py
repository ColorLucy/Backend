from django.db import models
from django.db.models import Max


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.id_categoria:
            max_id = Categoria.objects.aggregate(max_id=Max('id_categoria'))['max_id']
            self.id_categoria = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    fabricante = models.CharField(max_length=100)
    descripcion = models.TextField(null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column="id_categoria")

    def save(self, *args, **kwargs):
        if not self.id_producto:
            max_id = Producto.objects.aggregate(max_id=Max('id_producto'))['max_id']
            self.id_producto = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descripcion


class Detalle(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column="id_producto")

    def save(self, *args, **kwargs):
        if not self.id_detalle:
            max_id = Detalle.objects.aggregate(max_id=Max('id_detalle'))['max_id']
            self.id_detalle = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Imagen(models.Model):
    id_imagen = models.AutoField(primary_key=True)
    url = models.URLField()
    detalle = models.ForeignKey(Detalle, on_delete=models.CASCADE, db_column="id_detalle", related_name="imagenes")

    def save(self, *args, **kwargs):
        if not self.id_imagen:
            max_id = Imagen.objects.aggregate(max_id=Max('id_imagen'))['max_id']
            self.id_imagen = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.url

