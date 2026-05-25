from django.conf import settings
from django.db import models


class Nivel(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    valor = models.PositiveSmallIntegerField(unique=True, help_text="Valor numérico de la jerarquía (a mayor número, mayor autoridad)")

    class Meta:
        verbose_name = "Nivel"
        verbose_name_plural = "Niveles"
        db_table = "niveles"

    def __str__(self):
        return f"{self.nombre} ({self.valor})"


class Cargo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    nivel = models.ForeignKey(Nivel, on_delete=models.PROTECT, related_name='cargos', null=True)
    departamento = models.ForeignKey('Departamento', on_delete=models.SET_NULL, null=True, blank=True, related_name='cargos')
    superior = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='cargos_dependientes')

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        db_table = "cargos"

    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    sigla = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        db_table = "departamentos"

    def __str__(self):
        return self.nombre

class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='persona')
    cargo = models.ForeignKey(Cargo, null=True, blank=True, on_delete=models.SET_NULL, related_name='personas')
    departamento = models.ForeignKey(Departamento, null=True, blank=True, on_delete=models.SET_NULL, related_name='personas')
    superior = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinados')
    dni = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=150)
    apellido_paterno = models.CharField(max_length=150)
    apellido_materno = models.CharField(max_length=150, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        db_table = "personas"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}".strip()

    def __str__(self):
        return f"{self.nombre_completo} ({self.dni})"
