"""
Configuración de desarrollo para el Sistema de Servicio Técnico
"""

from .settings import *

# =========================
# DESARROLLO
# =========================
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ⚠️ IMPORTANTE:
# NO redefinimos DATABASES
# Se usa PostgreSQL desde settings.py

# =========================
# ARCHIVOS ESTÁTICOS
# =========================
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# =========================
# LOGGING (DESARROLLO)
# =========================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# =========================
# EMAIL (DESARROLLO)
# =========================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# =========================
# CACHE (DESARROLLO)
# =========================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# =========================
# SESIONES
# =========================
SESSION_COOKIE_AGE = 86400
SESSION_SAVE_EVERY_REQUEST = True

# =========================
# MEDIA
# =========================
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# =========================
# SEGURIDAD RELAJADA (DEV)
# =========================
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
X_FRAME_OPTIONS = 'SAMEORIGIN'
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
