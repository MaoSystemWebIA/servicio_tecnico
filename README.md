#  Sistema de Servicio Técnico

![Dashboard](https://github.com/user-attachments/assets/646484d7-0132-4640-8bc9-6667dba0858f)

Sistema completo de gestión para talleres de servicio técnico con **Inteligencia Artificial integrada**, desarrollado con Django 5.2.

##  Características Principales

###  Funcionalidades Avanzadas
- **Asistente IA**: Chatbot integrado para consultas rápidas sobre tickets, clientes y equipos
- **Predicción de Inventario**: Gráficos predictivos con Chart.js para gestión proactiva
- **Diagnóstico Inteligente**: Análisis automático de problemas con porcentajes de probabilidad
- **Alertas Inteligentes**: Notificaciones con cálculo de días hasta agotamiento de stock
- **Dashboard Interactivo**: Panel de control en tiempo real con métricas clave

###  Módulos Core
-  **Gestión de Clientes**: Registro completo con créditos y límites
-  **Gestión de Equipos**: Control de equipos con garantías y mantenimiento
-  **Tickets de Servicio**: Seguimiento completo del ciclo de vida
-  **Inventario Inteligente**: Control de stock con predicciones y alertas
-  **Proveedores**: Gestión completa de proveedores y compras
-  **Facturación**: Emisión de facturas electrónicas
-  **Reportes**: Generación de reportes y estadísticas avanzadas

##  Tecnologías

- **Backend**: Django 5.2.6
- **Base de Datos**: PostgreSQL 12+
- **Frontend**: Bootstrap 5, Chart.js 4.4
- **IA**: Sistema de procesamiento de lenguaje natural
- **Deployment**: Gunicorn, WhiteNoise
- **Python**: 3.12+

##  Requisitos del Sistema

- Python 3.12 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

##  Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/servicio-tecnico.git
cd servicio-tecnico
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos PostgreSQL
```sql
CREATE DATABASE servicio_tecnico_db;
CREATE USER servicio_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE servicio_tecnico_db TO servicio_user;
```

### 5. Configurar variables de entorno
```bash
cp env.example .env
```

Editar `.env` con tus configuraciones:
```env
DATABASE_URL=postgresql://servicio_user:tu_password@localhost:5432/servicio_tecnico_db
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Ejecutar migraciones
```bash
python manage.py migrate
```

### 7. Crear superusuario
```bash
python manage.py createsuperuser
```

### 8. Recopilar archivos estáticos
```bash
python manage.py collectstatic --noinput
```

### 9. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

Acceder a: `http://localhost:8000`

##  Despliegue en Producción

### Opción 1: Heroku

```bash
# 1. Instalar Heroku CLI
# Descargar desde: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Crear aplicación
heroku create tu-app-servicio-tecnico

# 4. Configurar variables de entorno
heroku config:set SECRET_KEY=tu-clave-secreta
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=tu-app-servicio-tecnico.herokuapp.com

# 5. Configurar base de datos
heroku addons:create heroku-postgresql:hobby-dev

# 6. Desplegar
git push heroku main

# 7. Ejecutar migraciones
heroku run python manage.py migrate

# 8. Crear superusuario
heroku run python manage.py createsuperuser
```

### Opción 2: Servidor VPS

```bash
# 1. Instalar dependencias del sistema
sudo apt update
sudo apt install python3-pip python3-venv postgresql nginx

# 2. Configurar PostgreSQL
sudo -u postgres createdb servicio_tecnico_db
sudo -u postgres createuser servicio_user

# 3. Clonar y configurar proyecto
git clone https://github.com/tu-usuario/servicio-tecnico.git
cd servicio-tecnico
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configurar .env
nano .env
# Agregar configuraciones de producción

# 5. Migraciones
python manage.py migrate
python manage.py collectstatic --noinput

# 6. Ejecutar con Gunicorn
gunicorn servicio_tecnico.wsgi:application --bind 0.0.0.0:8000
```

##  Capturas de Pantalla

- **Dashboard Interactivo**: Panel de control con métricas en tiempo real
- **Asistente IA**: Chatbot integrado para consultas rápidas
- **Predicción de Inventario**: Gráficos predictivos con tendencias
- **Diagnóstico Inteligente**: Análisis automático de problemas técnicos

##  Uso del Sistema

### Acceso Inicial
1. Ir a `http://localhost:8000`
2. Iniciar sesión con el superusuario creado
3. Configurar la empresa en **Configuración**

### Asistente IA
- Hacer preguntas sobre tickets, clientes, equipos o inventario
- Ejemplos:
  - "¿Qué ticket está retrasado?"
  - "Información del ticket TKT-001"
  - "¿Cuántos clientes hay?"

### Dashboard
- Ver métricas en tiempo real
- Revisar tickets recientes
- Monitorear alertas de inventario
- Analizar predicciones de stock

##  Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

##  Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

##  Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Twitter: [@tu-twitter](https://twitter.com/tu-twitter)
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)

##  Agradecimientos

- Django Community
- Bootstrap Team
- Chart.js Contributors
- Todos los contribuidores de código abierto

##  Soporte

Para soporte técnico o reportar bugs:
- Crear un [issue](https://github.com/tu-usuario/servicio-tecnico/issues)
- Email: soporte@tudominio.com

##  Changelog

### v2.0.0 (Actual)
-  Asistente IA integrado
-  Predicción de inventario con gráficos
-  Diagnóstico inteligente
-  Alertas mejoradas con días de agotamiento
-  Dashboard rediseñado

### v1.0.0
- Versión inicial del sistema
- Módulos básicos implementados
- Interfaz responsive
