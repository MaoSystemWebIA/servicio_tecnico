"""
Script para crear un video demo con el frontend real de la aplicación
Usa screenshots reales capturados del navegador
"""

from pathlib import Path
import time

def crear_video_desde_screenshots_reales():
    """Crea un video desde screenshots reales del frontend"""
    demo_dir = Path(__file__).parent
    frames_dir = demo_dir / "frames_reales"
    output_video = demo_dir / "demo-video-real.mp4"
    
    # Si no hay screenshots reales, usar los placeholders
    if not frames_dir.exists() or not list(frames_dir.glob("*.png")):
        print("No se encontraron screenshots reales.")
        print("Usando screenshots de placeholder...")
        frames_dir = demo_dir / "frames"
    
    try:
        from moviepy import ImageSequenceClip
        
        # Obtener todas las imágenes ordenadas
        images = sorted([str(f) for f in frames_dir.glob("*.png")])
        
        if not images:
            print("Error: No se encontraron imágenes")
            return
        
        print(f"Encontradas {len(images)} imágenes")
        print("Generando video con frontend real...")
        
        # Crear clip (3 segundos por imagen para que se vea mejor)
        clip = ImageSequenceClip(images, fps=1/3)  # 1/3 fps = 3 segundos por imagen
        
        # Escribir video
        clip.write_videofile(str(output_video), fps=24, codec='libx264')
        print(f"\nVideo creado exitosamente: {output_video}")
        print(f"Tamaño: {output_video.stat().st_size / (1024*1024):.2f} MB")
        
    except ImportError:
        print("Error: moviepy no está instalado")
        print("Instala con: pip install moviepy")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_video_desde_screenshots_reales()
