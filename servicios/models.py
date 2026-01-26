from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# ==================== USUARIOS ====================
class PerfilUsuario(models.Model):
    TIPOS_TECNICO = [
        ('senior', 'Técnico Senior'),
        ('junior', 'Técnico Junior'),
        ('auxiliar', 'Auxiliar'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_tecnico = models.CharField(max_length=20, choices=TIPOS_TECNICO, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    costo_hora = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fecha_contratacion = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.username


# ==================== CLIENTES ====================
class Cliente(models.Model):
    TIPOS_CLIENTE = [
        ('individual', 'Individual'),
        ('empresa', 'Empresa'),
        ('gobierno', 'Gobierno'),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS_CLIENTE)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    credito = models.BooleanField(default=False)
    limite_credito = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre


# ==================== EQUIPOS ====================
class Equipo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_equipo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.marca} {self.modelo}"


# ==================== TICKETS ====================
class TicketServicio(models.Model):
    ESTADOS = [
        ('recibido', 'Recibido'),
        ('reparacion', 'En Reparación'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.numero}"


# ==================== INVENTARIO ====================
class CategoriaRepuesto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Repuesto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaRepuesto, on_delete=models.CASCADE)
    stock = models.IntegerField()
    consumo_mensual = models.IntegerField()

    def dias_restantes(self):
        if self.consumo_mensual == 0:
            return None
        return round(self.stock / (self.consumo_mensual / 30), 1)

    def __str__(self):
        return self.nombre


# ==================== CONFIGURACIÓN ====================
class ConfiguracionSistema(models.Model):
    nombre_empresa = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionSistema.objects.exists():
            raise ValidationError("Solo puede existir una configuración")
        super().save(*args, **kwargs)

    def __str__(self):
        return "Configuración del Sistema"
