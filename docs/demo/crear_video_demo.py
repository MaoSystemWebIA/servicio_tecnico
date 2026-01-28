"""
Script para crear un video demo de la aplicación
Este script genera un video básico con información sobre las funcionalidades
"""

import os
from pathlib import Path

def crear_guion_demo():
    """Crea un guion para el video demo"""
    guion = """
# Guion para Video Demo - Sistema de Gestión para Talleres de Servicio Técnico

## Introducción (0:00 - 0:30)
- Presentación del sistema
- Características principales
- Tecnologías utilizadas

## 1. Dashboard (0:30 - 1:30)
- Panel de control en tiempo real
- Métricas clave
- Gráficos y estadísticas
- Tickets recientes
- Alertas de inventario

## 2. Gestión de Clientes (1:30 - 2:30)
- Lista de clientes
- Crear nuevo cliente
- Ver detalles del cliente
- Editar información
- Historial de servicios

## 3. Gestión de Equipos (2:30 - 3:30)
- Lista de equipos
- Registrar nuevo equipo
- Información de garantías
- Historial de reparaciones
- Asociación con clientes

## 4. Sistema de Tickets (3:30 - 5:00)
- Crear nuevo ticket
- Estados del ticket (Pendiente, En Proceso, Completado)
- Asignar técnico
- Agregar notas y comentarios
- Seguimiento del progreso
- Cerrar ticket

## 5. Inventario Inteligente (5:00 - 6:00)
- Lista de repuestos
- Control de stock
- Alertas de stock bajo
- Predicciones de inventario
- Gráficos de consumo

## 6. Chatbot con IA (6:00 - 6:30)
- Acceso al chatbot
- Consultas sobre tickets
- Consultas sobre clientes
- Consultas sobre inventario
- Respuestas inteligentes

## 7. Proveedores (6:30 - 7:00)
- Gestión de proveedores
- Información de contacto
- Historial de compras

## 8. Facturación (7:00 - 7:30)
- Generar facturas
- Asociar a tickets
- Exportar facturas
- Historial de facturación

## 9. Reportes (7:30 - 8:00)
- Generar reportes
- Estadísticas de servicios
- Análisis de rendimiento
- Exportar datos

## 10. Configuración (8:00 - 8:30)
- Configuración del sistema
- Datos de la empresa
- Personalización

## Conclusión (8:30 - 9:00)
- Resumen de funcionalidades
- Beneficios del sistema
- Información de contacto
"""
    return guion

def crear_instrucciones_grabacion():
    """Crea instrucciones detalladas para grabar el video"""
    instrucciones = """
# Instrucciones para Grabar el Video Demo

## Herramientas Recomendadas

### Opción 1: OBS Studio (Recomendado - Gratis)
1. Descargar OBS Studio: https://obsproject.com/
2. Configurar fuente de pantalla
3. Configurar audio (opcional)
4. Grabar en formato MP4

### Opción 2: Windows Game Bar (Windows 10/11)
1. Presionar Win + G
2. Click en el botón de grabación
3. O usar Win + Alt + R para iniciar grabación

### Opción 3: PowerPoint
1. Insertar > Grabar pantalla
2. Seleccionar área
3. Grabar y exportar como video

## Pasos para Grabar

1. **Preparar el entorno:**
   - Iniciar el servidor: `python manage.py runserver`
   - Abrir navegador en: http://localhost:8000
   - Iniciar sesión con credenciales de prueba

2. **Configurar la grabación:**
   - Resolución: 1920x1080 (Full HD) o 1280x720 (HD)
   - FPS: 30 fps
   - Formato: MP4
   - Audio: Opcional (música de fondo suave)

3. **Seguir el guion:**
   - Navegar por cada sección según el guion
   - Mostrar las funcionalidades principales
   - Hablar claro y pausado (si incluyes audio)
   - Hacer transiciones suaves entre secciones

4. **Duración recomendada:**
   - Total: 8-10 minutos
   - Cada sección: 30-90 segundos

5. **Edición (opcional):**
   - Agregar títulos al inicio
   - Agregar transiciones
   - Agregar música de fondo
   - Agregar texto explicativo

6. **Exportar:**
   - Formato: MP4
   - Resolución: 1920x1080 o 1280x720
   - Nombre: demo-video.mp4
   - Guardar en: docs/demo/demo-video.mp4

## Consejos

- Usa datos de ejemplo realistas
- Muestra las características más importantes
- Mantén un ritmo constante
- Evita pausas largas
- Muestra tanto éxito como manejo de errores
- Incluye el chatbot con IA si es posible
"""
    return instrucciones

if __name__ == "__main__":
    # Crear directorio si no existe
    demo_dir = Path(__file__).parent
    demo_dir.mkdir(parents=True, exist_ok=True)
    
    # Crear archivos de guion e instrucciones
    guion_path = demo_dir / "GUION_DEMO.md"
    instrucciones_path = demo_dir / "INSTRUCCIONES_GRABACION.md"
    
    with open(guion_path, 'w', encoding='utf-8') as f:
        f.write(crear_guion_demo())
    
    with open(instrucciones_path, 'w', encoding='utf-8') as f:
        f.write(crear_instrucciones_grabacion())
    
    print("Archivos creados:")
    print(f"   - {guion_path}")
    print(f"   - {instrucciones_path}")
    print("\nSigue las instrucciones para grabar el video demo")
