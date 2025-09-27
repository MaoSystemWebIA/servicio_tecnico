from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# ==================== MÓDULO DE USUARIOS Y PERFILES ====================
class PerfilUsuario(models.Model):
    TIPOS_TECNICO = (
        ('senior', 'Técnico Senior'),
        ('junior', 'Técnico Junior'),
        ('auxiliar', 'Auxiliar'),
    )
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_tecnico = models.CharField(max_length=20, choices=TIPOS_TECNICO, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    costo_hora = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fecha_contratacion = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_tecnico_display()}"

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

# ==================== MÓDULO DE CLIENTES ====================
class Cliente(models.Model):
    TIPOS_CLIENTE = (
        ('individual', 'Individual'),
        ('empresa', 'Empresa'),
        ('gobierno', 'Gobierno'),
    )
    
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS_CLIENTE)
    contacto = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    ruc_ci = models.CharField(max_length=20, blank=True)
    credito = models.BooleanField(default=False)
    limite_credito = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notas = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

# ==================== MÓDULO DE EQUIPOS ====================
class Equipo(models.Model):
    ESTADOS = (
        ('operativo', 'Operativo'),
        ('reparacion', 'En Reparación'),
        ('baja', 'De Baja'),
    )
    
    PRIORIDADES = (
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_equipo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100, unique=True)
    fecha_compra = models.DateField(null=True, blank=True)
    garantia_fabricante = models.DateField(null=True, blank=True)
    garantia_taller = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES)
    caracteristicas = models.TextField(blank=True)
    ubicacion = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.numero_serie}"

# ==================== MÓDULO DE TICKETS/SERVICIOS ====================
class TicketServicio(models.Model):
    ESTADOS_TICKET = (
        ('recibido', 'Recibido'),
        ('diagnostico', 'En Diagnóstico'),
        ('espera_aprobacion', 'Espera Aprobación'),
        ('reparacion', 'En Reparación'),
        ('espera_repuestos', 'Espera Repuestos'),
        ('completado', 'Completado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )
    
    numero = models.CharField(max_length=20, unique=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_prometida = models.DateTimeField(null=True, blank=True)
    problema_reportado = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS_TICKET, default='recibido')
    prioridad = models.CharField(max_length=20, choices=Equipo.PRIORIDADES)
    tecnico_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_real = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"Ticket {self.numero} - {self.equipo}"

# ==================== MÓDULO DE INVENTARIO ====================
class CategoriaRepuesto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class Repuesto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(CategoriaRepuesto, on_delete=models.CASCADE)
    marca = models.CharField(max_length=100, blank=True)
    modelo_compatible = models.CharField(max_length=200, blank=True)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    ubicacion_almacen = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

# ==================== MÓDULO DE PROVEEDORES ====================
class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    ruc = models.CharField(max_length=20, blank=True)
    tiempo_entrega = models.IntegerField(default=7)  # días
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3
    )
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

# ==================== MÓDULO DE FACTURACIÓN ====================
class Factura(models.Model):
    ESTADOS_FACTURA = (
        ('pendiente', 'Pendiente de Pago'),
        ('parcial', 'Pago Parcial'),
        ('pagada', 'Pagada'),
        ('cancelada', 'Cancelada'),
    )
    
    numero = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateTimeField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS_FACTURA, default='pendiente')
    ticket = models.ForeignKey(TicketServicio, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Factura {self.numero} - {self.cliente}"

# ==================== MÓDULO DE GASTOS ====================
class Gasto(models.Model):
    CATEGORIAS_GASTO = (
        ('reparacion', 'Reparación'),
        ('mantenimiento', 'Mantenimiento'),
        ('administrativo', 'Administrativo'),
        ('insumos', 'Insumos'),
        ('otros', 'Otros'),
    )
    
    descripcion = models.CharField(max_length=255)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_GASTO)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(default=timezone.now)
    ticket = models.ForeignKey(TicketServicio, on_delete=models.SET_NULL, null=True, blank=True)
    comprobante = models.FileField(upload_to='comprobantes/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.descripcion} - ${self.monto}"

# ==================== MÓDULO DE ALERTAS ====================
class Alerta(models.Model):
    TIPOS_ALERTA = (
        ('stock', 'Stock Bajo'),
        ('vencimiento', 'Vencimiento'),
        ('mantenimiento', 'Mantenimiento'),
        ('ticket', 'Ticket Urgente'),
        ('pago', 'Pago Pendiente'),
    )
    
    PRIORIDADES_ALERTA = (
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    )
    
    tipo = models.CharField(max_length=20, choices=TIPOS_ALERTA)
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES_ALERTA)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_vence = models.DateTimeField(null=True, blank=True)
    leida = models.BooleanField(default=False)
    usuario_destino = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"

# ==================== MÓDULO DE GARANTÍAS ====================
class Garantia(models.Model):
    TIPOS_GARANTIA = (
        ('fabricante', 'Garantía de Fabricante'),
        ('taller', 'Garantía de Taller'),
        ('reparacion', 'Garantía de Reparación'),
    )
    
    ticket = models.ForeignKey(TicketServicio, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS_GARANTIA)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    duracion_meses = models.IntegerField()
    terminos = models.TextField()
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Garantía {self.ticket.numero} - {self.get_tipo_display()}"

# ==================== MÓDULO DE MANTENIMIENTO PREVENTIVO ====================
class MantenimientoPreventivo(models.Model):
    FRECUENCIAS = (
        ('diario', 'Diario'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    )
    
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    descripcion = models.TextField()
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIAS)
    ultimo_mantenimiento = models.DateTimeField(null=True, blank=True)
    proximo_mantenimiento = models.DateTimeField(null=True, blank=True)
    tecnico_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    horas_estimadas = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Mantenimiento {self.equipo} - {self.frecuencia}"

# ==================== MÓDULO DE REPORTES ====================
class Reporte(models.Model):
    TIPOS_REPORTE = (
        ('servicios', 'Reporte de Servicios'),
        ('financiero', 'Reporte Financiero'),
        ('inventario', 'Reporte de Inventario'),
        ('productividad', 'Productividad de Técnicos'),
        ('clientes', 'Reporte de Clientes'),
    )
    
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS_REPORTE)
    parametros = models.JSONField(default=dict)  # Filtros y configuraciones
    fecha_creacion = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='reportes/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_display()}"

# ==================== MÓDULO DE CONFIGURACIÓN ====================
class ConfiguracionSistema(models.Model):
    nombre_empresa = models.CharField(max_length=200, default="Servicio Técnico")
    ruc_empresa = models.CharField(max_length=20, blank=True)
    direccion_empresa = models.TextField(blank=True)
    telefono_empresa = models.CharField(max_length=50, blank=True)
    email_empresa = models.EmailField(blank=True)
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)
    logo = models.ImageField(upload_to='configuracion/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Permitir solo una instancia de configuración
        if not self.pk and ConfiguracionSistema.objects.exists():
            raise ValidationError('Solo puede existir una configuración del sistema')
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return "Configuración del Sistema"
