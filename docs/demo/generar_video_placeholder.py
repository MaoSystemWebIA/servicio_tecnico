"""
Script para generar un video placeholder del demo
Este script crea un video básico con información sobre la aplicación
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    from pathlib import Path
    import subprocess
    import sys
    
    def crear_imagen_placeholder(texto, numero, total, output_path):
        """Crea una imagen placeholder con texto"""
        # Crear imagen
        width, height = 1920, 1080
        img = Image.new('RGB', (width, height), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # Intentar cargar fuente, si no usar default
        try:
            font_titulo = ImageFont.truetype("arial.ttf", 80)
            font_texto = ImageFont.truetype("arial.ttf", 40)
        except:
            font_titulo = ImageFont.load_default()
            font_texto = ImageFont.load_default()
        
        # Título
        titulo = "Sistema de Gestión para Talleres de Servicio Técnico"
        bbox = draw.textbbox((0, 0), titulo, font=font_titulo)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(((width - text_width) / 2, 200), titulo, fill='#ffffff', font=font_titulo)
        
        # Texto principal
        bbox = draw.textbbox((0, 0), texto, font=font_texto)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, 500), texto, fill='#0ea5e9', font=font_texto)
        
        # Progreso
        progreso = f"Slide {numero} de {total}"
        bbox = draw.textbbox((0, 0), progreso, font=font_texto)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, 800), progreso, fill='#64748b', font=font_texto)
        
        # Guardar
        img.save(output_path, 'PNG')
        print(f"Imagen creada: {output_path}")
    
    def crear_video_desde_imagenes():
        """Crea un video desde las imágenes generadas"""
        demo_dir = Path(__file__).parent
        frames_dir = demo_dir / "frames"
        frames_dir.mkdir(exist_ok=True)
        
        # Slides del demo
        slides = [
            "Bienvenido al Sistema de Gestión para Talleres",
            "Dashboard en Tiempo Real con Métricas Clave",
            "Gestión Completa de Clientes y Equipos",
            "Sistema de Tickets con Seguimiento Detallado",
            "Inventario Inteligente con Predicciones",
            "Chatbot con IA para Consultas Rápidas",
            "Gestión de Proveedores y Compras",
            "Facturación Electrónica Automática",
            "Reportes y Estadísticas Avanzadas",
            "Configuración Personalizable del Sistema"
        ]
        
        # Crear imágenes
        print("Generando imágenes...")
        for i, slide in enumerate(slides, 1):
            img_path = frames_dir / f"slide_{i:02d}.png"
            crear_imagen_placeholder(slide, i, len(slides), img_path)
        
        print(f"\n{len(slides)} imágenes creadas en: {frames_dir}")
        print("\nPara crear el video, necesitas instalar moviepy:")
        print("  pip install moviepy")
        print("\nLuego ejecuta el script crear_video_final.py")
        
        # Crear script para generar video final
        script_video = demo_dir / "crear_video_final.py"
        with open(script_video, 'w', encoding='utf-8') as f:
            f.write('''"""
Script para crear el video final desde las imágenes
Requiere: pip install moviepy
"""
try:
    from moviepy.editor import ImageSequenceClip
    from pathlib import Path
    
    demo_dir = Path(__file__).parent
    frames_dir = demo_dir / "frames"
    output_video = demo_dir / "demo-video.mp4"
    
    # Obtener todas las imágenes ordenadas
    images = sorted([str(f) for f in frames_dir.glob("slide_*.png")])
    
    # Crear clip (2 segundos por imagen)
    clip = ImageSequenceClip(images, fps=0.5)  # 0.5 fps = 2 segundos por imagen
    
    # Escribir video
    print("Generando video...")
    clip.write_videofile(str(output_video), fps=24, codec='libx264')
    print(f"Video creado: {output_video}")
    
except ImportError:
    print("Error: moviepy no está instalado")
    print("Instala con: pip install moviepy")
except Exception as e:
    print(f"Error: {e}")
''')
        print(f"\nScript de video creado: {script_video}")
    
    if __name__ == "__main__":
        crear_video_desde_imagenes()
        
except ImportError as e:
    print(f"Error: {e}")
    print("Pillow está instalado, pero hay un problema.")
    print("\nPara crear el video demo manualmente:")
    print("1. Usa OBS Studio o Windows Game Bar para grabar")
    print("2. Sigue el guion en GUION_DEMO.md")
    print("3. Guarda el video como: docs/demo/demo-video.mp4")
