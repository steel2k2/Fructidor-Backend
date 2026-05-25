from django.db import migrations, models
import django.db.models.deletion

def setup_ti_data(apps, schema_editor):
    # Obtenemos los modelos desde el registro de la migración
    Departamento = apps.get_model('accounts', 'Departamento')
    Cargo = apps.get_model('accounts', 'Cargo')
    Nivel = apps.get_model('accounts', 'Nivel')
    Person = apps.get_model('accounts', 'Person')
    User = apps.get_model('auth', 'User')

    # 1. Crear el Departamento de TI
    depto_ti, _ = Departamento.objects.get_or_create(
        nombre="Dirección de Tecnologías de la Información",
        defaults={'sigla': 'DTI'}
    )

    # 2. Obtener Niveles de autoridad (creados en la migración 0006)
    try:
        nivel_admin = Nivel.objects.get(valor=100)
        nivel_supervisor = Nivel.objects.get(valor=50)
    except Nivel.DoesNotExist:
        # Si por alguna razón no existen, detenemos la ejecución para evitar errores
        return

    # 3. Crear el cargo de Director
    director_ti, _ = Cargo.objects.get_or_create(
        nombre="Director de Tecnologías de Información",
        defaults={
            'descripcion': 'Responsable máximo de la planificación y estrategia tecnológica institucional.',
            'nivel': nivel_admin,
            'departamento': depto_ti
        }
    )

    # 4. Crear el cargo de Jefe dependiendo del Director
    Cargo.objects.get_or_create(
        nombre="Jefe de Desarrollo de Sistemas",
        defaults={
            'descripcion': 'Lidera los equipos de desarrollo y mantenimiento de software.',
            'nivel': nivel_supervisor,
            'departamento': depto_ti,
            'superior': director_ti
        }
    )

    # 5. Asignar el cargo de Director y su departamento al usuario 'achana'
    try:
        user_achana = User.objects.get(username='achana')
        persona_achana = Person.objects.get(user=user_achana)
        persona_achana.cargo = director_ti
        persona_achana.departamento = depto_ti
        persona_achana.save()
    except (User.DoesNotExist, Person.DoesNotExist):
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_cargo_departamento'), # Aseguramos que el campo 'departamento' en Cargo ya exista
    ]

    operations = [
        migrations.RunPython(setup_ti_data),
    ]