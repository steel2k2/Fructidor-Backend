from django.contrib import admin

from .models import Person, Role


admin.site.register(Role)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'dni', 'nombres', 'apellidos', 'fecha_nacimiento', 'role')
    search_fields = ('user__username', 'dni', 'nombres', 'apellidos')
