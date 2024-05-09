from django.db import models
from django.db.models import Max
from cloudinary.models import CloudinaryField

CLOUDINARY_ROOT_URL = "https://res.cloudinary.com/dhhnv3njc/"


class HomeText(models.Model):
    id = models.AutoField(primary_key=True)
    start_title = models.CharField(max_length=100)
    start_text_one = models.CharField(max_length=100)
    start_text_two = models.CharField(max_length=100)
    combinations_title = models.CharField(max_length=100)
    combinations_text = models.CharField(max_length=100)
    products_text = models.CharField(max_length=100)
    allies_text = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.id:
            max_id = HomeText.objects.aggregate(max_id=Max("id"))["max_id"]
            self.id = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.start_title


class HomeStartImage(models.Model):
    id = models.AutoField(primary_key=True)
    start_image = CloudinaryField(
        folder="informacion/",
        overwrite=True,
        resource_type="image",
        use_filename=True,
    )

    @property
    def url(self):
        return f"{CLOUDINARY_ROOT_URL}{self.start_image}"

    def save(self, *args, **kwargs):
        if not self.id:
            max_id = HomeStartImage.objects.aggregate(max_id=Max("id"))["max_id"]
            self.id = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id


class HomeCombinationsImage(models.Model):
    id = models.AutoField(primary_key=True)
    combinations_image = CloudinaryField(
        folder="informacion/",
        overwrite=True,
        resource_type="image",
        use_filename=True,
    )

    @property
    def url(self):
        return f"{CLOUDINARY_ROOT_URL}{self.combinations_image}"

    def save(self, *args, **kwargs):
        if not self.id:
            max_id = HomeCombinationsImage.objects.aggregate(max_id=Max("id"))["max_id"]
            self.id = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id


class HomeProductsImage(models.Model):
    id = models.AutoField(primary_key=True)
    products_image = CloudinaryField(
        folder="informacion/",
        overwrite=True,
        resource_type="image",
        use_filename=True,
    )

    @property
    def url(self):
        return f"{CLOUDINARY_ROOT_URL}{self.products_image}"

    def save(self, *args, **kwargs):
        if not self.id:
            max_id = HomeProductsImage.objects.aggregate(max_id=Max("id"))["max_id"]
            self.id = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id


class HomeAlliesImage(models.Model):
    id = models.AutoField(primary_key=True)
    allies_image = CloudinaryField(
        folder="informacion/",
        overwrite=True,
        resource_type="image",
        use_filename=True,
    )

    @property
    def url(self):
        return f"{CLOUDINARY_ROOT_URL}{self.allies_image}"

    def save(self, *args, **kwargs):
        if not self.id:
            max_id = HomeAlliesImage.objects.aggregate(max_id=Max("id"))["max_id"]
            self.id = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id


class InfoBar(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    phone_one = models.CharField(max_length=100)
    phone_two = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.id:
            max_id = InfoBar.objects.aggregate(max_id=Max("id"))["max_id"]
            self.id = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
