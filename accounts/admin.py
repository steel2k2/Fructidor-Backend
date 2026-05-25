from django.contrib import admin

from .models import Person, Cargo, Nivel, Departamento


@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'valor')
    ordering = ('-valor',)


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento', 'nivel', 'superior')
    list_filter = ('nivel', 'departamento')
    ordering = ('-nivel__valor',)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sigla')
    search_fields = ('nombre', 'sigla')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'dni', 'nombres', 'apellido_paterno', 'apellido_materno', 'cargo', 'departamento', 'superior')
    search_fields = ('user__username', 'dni', 'nombres', 'apellido_paterno', 'apellido_materno')
