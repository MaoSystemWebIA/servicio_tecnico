from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    PerfilUsuario, Especialidad, Cliente, Equipo, TicketServicio,
    CategoriaRepuesto, Repuesto, Proveedor, Factura, Gasto,
    Alerta, Garantia, MantenimientoPreventivo, Reporte,
    ConfiguracionSistema
)

# ==================== ADMINISTRACIÓN DE USUARIOS ====================
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_tecnico', 'telefono', 'costo_hora', 'activo')
    list_filter = ('tipo_tecnico', 'activo')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name')

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# ==================== ADMINISTRACIÓN DE CLIENTES ====================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo', 'telefono', 'email', 'credito', 'fecha_registro')
    list_filter = ('tipo', 'credito', 'fecha_registro')
    search_fields = ('codigo', 'nombre', 'ruc_ci', 'email')
    readonly_fields = ('fecha_registro',)

# ==================== ADMINISTRACIÓN DE EQUIPOS ====================
@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'numero_serie', 'cliente', 'estado', 'prioridad')
    list_filter = ('estado', 'prioridad', 'marca', 'tipo_equipo')
    search_fields = ('numero_serie', 'marca', 'modelo', 'cliente__nombre')
    raw_id_fields = ('cliente',)

# ==================== ADMINISTRACIÓN DE TICKETS ====================
@admin.register(TicketServicio)
class TicketServicioAdmin(admin.ModelAdmin):
    list_display = ('numero', 'equipo', 'estado', 'prioridad', 'tecnico_asignado', 'fecha_ingreso', 'costo_estimado')
    list_filter = ('estado', 'prioridad', 'fecha_ingreso', 'tecnico_asignado')
    search_fields = ('numero', 'equipo__numero_serie', 'equipo__cliente__nombre')
    raw_id_fields = ('equipo', 'tecnico_asignado')
    readonly_fields = ('numero', 'fecha_ingreso')

# ==================== ADMINISTRACIÓN DE INVENTARIO ====================
@admin.register(CategoriaRepuesto)
class CategoriaRepuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'stock_actual', 'stock_minimo', 'precio_venta')
    list_filter = ('categoria', 'marca')
    search_fields = ('codigo', 'nombre', 'marca', 'modelo_compatible')
    list_editable = ('stock_actual', 'precio_venta')

# ==================== ADMINISTRACIÓN DE PROVEEDORES ====================
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto', 'telefono', 'email', 'rating', 'activo')
    list_filter = ('rating', 'activo')
    search_fields = ('nombre', 'contacto', 'ruc')

# ==================== ADMINISTRACIÓN DE FACTURACIÓN ====================
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'fecha_emision', 'total', 'estado')
    list_filter = ('estado', 'fecha_emision')
    search_fields = ('numero', 'cliente__nombre')
    raw_id_fields = ('cliente', 'ticket')
    readonly_fields = ('numero', 'fecha_emision')

# ==================== ADMINISTRACIÓN DE GASTOS ====================
@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'categoria', 'monto', 'fecha', 'ticket')
    list_filter = ('categoria', 'fecha')
    search_fields = ('descripcion',)
    raw_id_fields = ('ticket',)

# ==================== ADMINISTRACIÓN DE ALERTAS ====================
@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'prioridad', 'fecha_creacion', 'leida', 'usuario_destino')
    list_filter = ('tipo', 'prioridad', 'leida', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    raw_id_fields = ('usuario_destino',)

# ==================== ADMINISTRACIÓN DE GARANTÍAS ====================
@admin.register(Garantia)
class GarantiaAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'tipo', 'fecha_inicio', 'fecha_fin', 'activa')
    list_filter = ('tipo', 'activa', 'fecha_inicio')
    search_fields = ('ticket__numero',)
    raw_id_fields = ('ticket',)

# ==================== ADMINISTRACIÓN DE MANTENIMIENTO ====================
@admin.register(MantenimientoPreventivo)
class MantenimientoPreventivoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'frecuencia', 'ultimo_mantenimiento', 'proximo_mantenimiento', 'activo')
    list_filter = ('frecuencia', 'activo', 'ultimo_mantenimiento')
    search_fields = ('equipo__numero_serie', 'equipo__cliente__nombre')
    raw_id_fields = ('equipo', 'tecnico_asignado')

# ==================== ADMINISTRACIÓN DE REPORTES ====================
@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'fecha_creacion', 'creado_por')
    list_filter = ('tipo', 'fecha_creacion')
    search_fields = ('nombre',)
    raw_id_fields = ('creado_por',)

# ==================== ADMINISTRACIÓN DE CONFIGURACIÓN ====================
@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'ruc_empresa', 'telefono_empresa', 'iva_porcentaje')
    
    def has_add_permission(self, request):
        # Solo permitir una instancia de configuración
        return not ConfiguracionSistema.objects.exists()
