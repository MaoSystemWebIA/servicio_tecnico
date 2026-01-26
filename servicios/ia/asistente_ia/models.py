from django.db import models


class Conversacion(models.Model):
    mensaje_usuario = models.TextField()
    respuesta_ia = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mensaje_usuario[:50]




# Create your models here.
