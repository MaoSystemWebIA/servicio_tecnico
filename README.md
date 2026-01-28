Sistema de Gestión para Talleres de Servicio Técnico

Sistema completo de gestión para talleres de servicio técnico con funcionalidades avanzadas, desarrollado con Django 5.2.

## 🎥 Demo en Video

Puedes ver una demostración completa de todas las funcionalidades del sistema en el siguiente video:

📹 **[Ver Demo Completo](docs/demo/demo-video.mp4)**

El video muestra todas las características principales del sistema, incluyendo el panel de control, gestión de tickets, inventario inteligente, chatbot con IA y más.

---

Características Principales

Funcionalidades Avanzadas:
Chatbot integrado para consultas rápidas sobre tickets, clientes y equipos
Gráficos predictivos para gestión proactiva de inventario
Análisis automático de problemas con porcentajes de probabilidad
Notificaciones inteligentes con cálculo de días hasta agotamiento de stock
Panel de control en tiempo real con métricas clave

Módulos Principales:
Gestión completa de clientes, equipos y tickets de servicio
Control de inventario con predicciones y alertas
Administración de proveedores y compras
Emisión de facturas electrónicas
Generación de reportes y estadísticas avanzadas

Tecnologías Utilizadas
Backend: Django 5.2.6
Base de datos: PostgreSQL 12+
Frontend: Bootstrap 5, Chart.js 4.4
Despliegue: Gunicorn, WhiteNoise

Python: 3.12+
Requisitos del Sistema
Python 3.12 o superior
PostgreSQL 12 o superior
pip (gestor de paquetes de Python)

Instalación Básica
Clonar el repositorio: git clone https://github.com/tu-usuario/servicio-tecnico.git
Crear y activar entorno virtual
Instalar dependencias: pip install -r requirements.txt
Configurar base de datos PostgreSQL
Configurar variables de entorno en archivo .env
Ejecutar migraciones: python manage.py migrate
Crear superusuario: python manage.py createsuperuser
Recopilar archivos estáticos
Ejecutar servidor: python manage.py runserver
Acceso inicial: http://localhost:8000

Despliegue en Producción
Opción 1: Heroku
Configurar aplicación Heroku con base de datos PostgreSQL
Establecer variables de entorno necesarias
Desplegar código y ejecutar migraciones

Opción 2: Servidor VPS
Instalar dependencias: Python, PostgreSQL, Nginx
Configurar base de datos PostgreSQL
Configurar entorno virtual y dependencias del proyecto
Ejecutar con Gunicorn y configurar Nginx como proxy inverso
Uso del Sistema
Acceder a la URL de instalación e iniciar sesión

Configurar datos de la empresa en la sección Configuración
Utilizar el chatbot para consultas rápidas sobre tickets, clientes o inventario
Monitorear métricas en el panel de control en tiempo real
Gestionar tickets, inventario, clientes y proveedores desde los módulos correspondientes

Contribuciones
Las contribuciones son bienvenidas mediante el proceso estándar de fork, creación de rama, commit y pull request.
Información Adicional
Licencia: MIT
Autor: Tu Nombre

Soporte: A través de issues en GitHub o correo electrónico
Historial de Versiones:
v2.0.0: Chatbot integrado, predicción de inventario, diagnóstico inteligente, alertas mejoradas
v1.0.0: Versión inicial con módulos básicos e interfaz responsive
