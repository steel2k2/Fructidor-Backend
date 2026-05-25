#!/usr/bin/env bash
# Salir inmediatamente si un comando falla
set -o errexit

# Instalar dependencias obligatorias
pip install -r requirements.txt

# Ejecutar migraciones automáticamente en Neon
python manage.py migrate

# Auto-crear el superusuario si modificaste el manage.py antes
# python manage.py ejecutar_script_si_fuese_necesario