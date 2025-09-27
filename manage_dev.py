#!/usr/bin/env python
"""
Script de gestión para desarrollo del Sistema de Servicio Técnico
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicio_tecnico.settings')
    django.setup()
    
    # Comandos útiles para desarrollo
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'setup':
            print("🚀 Configurando el Sistema de Servicio Técnico...")
            print("📦 Ejecutando migraciones...")
            execute_from_command_line(['manage.py', 'migrate'])
            
            print("👤 Creando superusuario...")
            execute_from_command_line(['manage.py', 'createsuperuser', '--username', 'admin', '--email', 'admin@serviciotecnico.com', '--noinput'])
            
            print("📁 Recopilando archivos estáticos...")
            execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
            
            print("✅ ¡Configuración completada!")
            print("🌐 Ejecuta 'python manage.py runserver' para iniciar el servidor")
            print("👤 Usuario: admin | Contraseña: admin123")
            
        elif command == 'reset':
            print("🔄 Reiniciando la base de datos...")
            execute_from_command_line(['manage.py', 'flush', '--noinput'])
            execute_from_command_line(['manage.py', 'migrate'])
            execute_from_command_line(['manage.py', 'createsuperuser', '--username', 'admin', '--email', 'admin@serviciotecnico.com', '--noinput'])
            print("✅ Base de datos reiniciada")
            
        else:
            execute_from_command_line(sys.argv)
    else:
        print("Sistema de Servicio Técnico - Script de Desarrollo")
        print("Comandos disponibles:")
        print("  python manage_dev.py setup    - Configurar el sistema completo")
        print("  python manage_dev.py reset    - Reiniciar la base de datos")
        print("  python manage_dev.py runserver - Iniciar servidor de desarrollo")
        print("  python manage_dev.py [comando] - Ejecutar comando Django normal")
