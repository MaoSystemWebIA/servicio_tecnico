# Sistema de Servicio Técnico

Un sistema completo de gestión para talleres de servicio técnico desarrollado con Django.

## Características

### Módulos Principales
- **Gestión de Clientes**: Registro y administración de clientes
- **Gestión de Equipos**: Control de equipos y dispositivos
- **Tickets de Servicio**: Seguimiento completo de servicios técnicos
- **Inventario**: Control de repuestos y stock
- **Proveedores**: Gestión de proveedores y compras
- **Facturación**: Emisión de facturas y control de pagos
- **Reportes**: Generación de reportes y estadísticas
- **Dashboard**: Panel de control con métricas importantes

### Funcionalidades
- ✅ Sistema de autenticación y autorización
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Gestión completa de tickets de servicio
- ✅ Control de inventario con alertas de stock bajo
- ✅ Sistema de garantías
- ✅ Mantenimiento preventivo
- ✅ Generación de reportes
- ✅ Interfaz responsive con Bootstrap 5
- ✅ Configuración para producción

## Requisitos del Sistema

- Python 3.12+
- PostgreSQL 12+
- Node.js (para compilar archivos estáticos)

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd servicio_tecnico
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
Crear una base de datos PostgreSQL:
```sql
CREATE DATABASE servicio_tecnico_db;
CREATE USER servicio_user WITH PASSWORD 'password_seguro';
GRANT ALL PRIVILEGES ON DATABASE servicio_tecnico_db TO servicio_user;
```

### 5. Configurar variables de entorno
Copiar el archivo de ejemplo y configurar:
```bash
cp env.example .env
```

Editar `.env` con tus configuraciones:
```env
DATABASE_URL=postgresql://servicio_user:password_seguro@localhost:5432/servicio_tecnico_db
SECRET_KEY=tu-clave-secreta-aqui
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
python manage.py collectstatic
```

### 9. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

## Configuración para Producción

### 1. Usar configuración de producción
```bash
export DJANGO_SETTINGS_MODULE=servicio_tecnico.settings_production
```

### 2. Configurar variables de entorno de producción
```env
DEBUG=False
SECRET_KEY=clave-secreta-muy-segura
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgresql://usuario:password@host:puerto/base_de_datos
```

### 3. Recopilar archivos estáticos
```bash
python manage.py collectstatic --noinput
```

### 4. Ejecutar con Gunicorn
```bash
gunicorn servicio_tecnico.wsgi:application --bind 0.0.0.0:8000
```

## Despliegue en Heroku

### 1. Instalar Heroku CLI
Descargar e instalar desde [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

### 2. Login en Heroku
```bash
heroku login
```

### 3. Crear aplicación
```bash
heroku create tu-app-servicio-tecnico
```

### 4. Configurar variables de entorno
```bash
heroku config:set SECRET_KEY=tu-clave-secreta
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=tu-app-servicio-tecnico.herokuapp.com
```

### 5. Configurar base de datos
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 6. Desplegar
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 7. Ejecutar migraciones
```bash
heroku run python manage.py migrate
```

### 8. Crear superusuario
```bash
heroku run python manage.py createsuperuser
```

## Estructura del Proyecto

```
servicio_tecnico/
├── core/                    # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas
│   ├── forms.py            # Formularios
│   ├── admin.py            # Administración Django
│   ├── urls.py             # URLs de la aplicación
│   └── templates/          # Templates HTML
├── servicio_tecnico/       # Configuración del proyecto
│   ├── settings.py         # Configuración desarrollo
│   ├── settings_production.py  # Configuración producción
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # WSGI
├── static/                 # Archivos estáticos
│   ├── css/               # Estilos CSS
│   └── js/                # JavaScript
├── templates/             # Templates base
├── media/                 # Archivos subidos por usuarios
├── requirements.txt       # Dependencias Python
├── Procfile              # Configuración Heroku
└── README.md             # Este archivo
```

## Uso del Sistema

### Acceso Inicial
1. Ir a `http://localhost:8000`
2. Iniciar sesión con el superusuario creado
3. Configurar la empresa en Configuración

### Gestión de Clientes
1. Ir a Clientes > Lista de Clientes
2. Crear nuevos clientes con información completa
3. Asociar equipos a cada cliente

### Gestión de Equipos
1. Ir a Equipos > Lista de Equipos
2. Registrar equipos con número de serie único
3. Establecer garantías y prioridades

### Tickets de Servicio
1. Ir a Tickets > Lista de Tickets
2. Crear tickets asociados a equipos
3. Asignar técnicos y establecer fechas prometidas
4. Seguir el flujo de estados del ticket

### Inventario
1. Ir a Inventario > Repuestos
2. Registrar repuestos con códigos únicos
3. Establecer stock mínimo para alertas
4. Actualizar precios regularmente

## Personalización

### Agregar Nuevos Módulos
1. Crear modelos en `core/models.py`
2. Agregar formularios en `core/forms.py`
3. Crear vistas en `core/views.py`
4. Configurar URLs en `core/urls.py`
5. Crear templates en `core/templates/`

### Modificar Estilos
- Editar `static/css/custom.css`
- Los estilos se basan en Bootstrap 5
- Usar variables CSS para colores principales

## Soporte

Para soporte técnico o reportar bugs:
- Crear un issue en el repositorio
- Contactar al desarrollador

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## Changelog

### v1.0.0
- Versión inicial del sistema
- Módulos básicos implementados
- Interfaz responsive
- Configuración para producción
