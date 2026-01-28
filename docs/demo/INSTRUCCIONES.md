# 📋 Instrucciones para subir el video demo a GitHub

## Pasos a seguir:

1. **Coloca tu video demo** en esta carpeta con el nombre: `demo-video.mp4`

2. **Abre una terminal** en la raíz del proyecto (`d:\servicio_tecnico`)

3. **Ejecuta los siguientes comandos:**

```bash
# Agregar los archivos nuevos
git add docs/demo/README.md
git add docs/demo/demo-video.mp4
git add README.md

# Hacer commit
git commit -m "Agregar video demo de la aplicación"

# Subir a GitHub
git push origin main
```

## ✅ Archivos que se subirán:

- ✅ `docs/demo/README.md` - Descripción del demo
- ✅ `docs/demo/demo-video.mp4` - Tu video demo (cuando lo agregues)
- ✅ `README.md` - Actualizado con enlace al video

## 📝 Nota:

El video se mostrará en el README principal del proyecto. Una vez subido, los usuarios podrán verlo directamente desde GitHub.
