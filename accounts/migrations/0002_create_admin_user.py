from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin_user(apps, schema_editor):
    # Obtenemos los modelos desde el registro de aplicaciones para asegurar compatibilidad
    User = apps.get_model('auth', 'User')
    Role = apps.get_model('accounts', 'Role')
    Person = apps.get_model('accounts', 'Person')

    # 1. Crear o asegurar que existe el rol de Administrador
    role, _ = Role.objects.get_or_create(
        name='Administrador',
        defaults={'description': 'Usuario con acceso total al sistema'}
    )

    # 2. Crear el superusuario si no existe
    username = 'achana'
    admin_user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': 'admin@fructidor.com',
            'is_superuser': True,
            'is_staff': True,
            'is_active': True
        }
    )
    # Forzamos la contraseña en ambos casos (nuevo o existente)
    admin_user.password = make_password('bolivia2026')
    admin_user.save()

    # 3. Asegurar el registro de Persona asociado
    Person.objects.get_or_create(
        user=admin_user,
        defaults={
            'role': role,
            'dni': 'ADMIN-01',
            'nombres': 'Admin',
            'apellidos': 'Principal'
        }
    )

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'), # Depende de que las tablas ya existan
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]