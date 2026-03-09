from django.db import models
from django.contrib.auth.hashers import make_password


class SuperAdmin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash on creation
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Super Admin'


class Seller(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    is_approved = models.BooleanField(default=False)
    face_data = models.CharField(max_length=500, blank=True, null=True)
    # face_data stores the path to the saved face image dataset folder

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Seller'


class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    face_data = models.CharField(max_length=500, blank=True, null=True)
    # face_data stores the path to the saved face image dataset folder

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Customer'
