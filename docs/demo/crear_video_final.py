"""
Script para crear el video final desde las imágenes
Requiere: pip install moviepy
"""
try:
    from moviepy import ImageSequenceClip
    from pathlib import Path
    
    demo_dir = Path(__file__).parent
    frames_dir = demo_dir / "frames"
    output_video = demo_dir / "demo-video.mp4"
    
    # Obtener todas las imágenes ordenadas
    images = sorted([str(f) for f in frames_dir.glob("slide_*.png")])
    
    if not images:
        print("Error: No se encontraron imágenes en frames/")
        exit(1)
    
    print(f"Encontradas {len(images)} imágenes")
    print("Generando video...")
    
    # Crear clip (2 segundos por imagen = 0.5 fps)
    clip = ImageSequenceClip(images, fps=0.5)
    
    # Escribir video
    clip.write_videofile(str(output_video), fps=24, codec='libx264')
    print(f"\nVideo creado exitosamente: {output_video}")
    print(f"Tamaño: {output_video.stat().st_size / (1024*1024):.2f} MB")
    
except ImportError as e:
    print(f"Error: moviepy no está instalado correctamente")
    print(f"Detalles: {e}")
    print("Instala con: pip install moviepy")
except Exception as e:
    print(f"Error al crear el video: {e}")
    import traceback
    traceback.print_exc()
