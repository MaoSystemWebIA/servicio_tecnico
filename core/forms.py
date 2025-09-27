from django import forms
from django.contrib.auth.models import User
from .models import (
    PerfilUsuario, Especialidad, Cliente, Equipo, TicketServicio,
    CategoriaRepuesto, Repuesto, Proveedor, Factura, Gasto,
    Alerta, Garantia, MantenimientoPreventivo, Reporte,
    ConfiguracionSistema
)

# ==================== USUARIOS ====================
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = '__all__'

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = '__all__'

# ==================== CLIENTES ====================
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

# ==================== EQUIPOS ====================
class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = '__all__'

# ==================== TICKETS ====================
class TicketServicioForm(forms.ModelForm):
    class Meta:
        model = TicketServicio
        fields = '__all__'

# ==================== INVENTARIO ====================
class CategoriaRepuestoForm(forms.ModelForm):
    class Meta:
        model = CategoriaRepuesto
        fields = '__all__'

class RepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = '__all__'

# ==================== PROVEEDORES ====================
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

# ==================== FACTURACIÓN ====================
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'

# ==================== GASTOS ====================
class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = '__all__'

# ==================== ALERTAS ====================
class AlertaForm(forms.ModelForm):
    class Meta:
        model = Alerta
        fields = '__all__'

# ==================== GARANTÍAS ====================
class GarantiaForm(forms.ModelForm):
    class Meta:
        model = Garantia
        fields = '__all__'

# ==================== MANTENIMIENTO PREVENTIVO ====================
class MantenimientoPreventivoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoPreventivo
        fields = '__all__'

# ==================== REPORTES ====================
class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = '__all__'

# ==================== CONFIGURACIÓN ====================
class ConfiguracionSistemaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionSistema
        fields = '__all__'
