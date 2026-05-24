from django.conf import settings
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        db_table = "roles"

    def __str__(self):
        return self.name


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='persona')
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL, related_name='persons')
    dni = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        db_table = "personas"

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.dni})"
