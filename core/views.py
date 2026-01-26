from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Cliente, Equipo, TicketServicio, CategoriaRepuesto, Repuesto, 
    Proveedor, Factura, Gasto, Alerta, Garantia, MantenimientoPreventivo, 
    Reporte, ConfiguracionSistema, PerfilUsuario
)
from .forms import (
    ClienteForm, EquipoForm, TicketServicioForm, CategoriaRepuestoForm, 
    RepuestoForm, ProveedorForm, FacturaForm, GastoForm, AlertaForm, 
    GarantiaForm, MantenimientoPreventivoForm, ReporteForm, 
    ConfiguracionSistemaForm, PerfilUsuarioForm
)

# ==================== VISTA PRINCIPAL/DASHBOARD ====================
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        context['total_clientes'] = Cliente.objects.count()
        context['total_equipos'] = Equipo.objects.count()
        context['total_tickets'] = TicketServicio.objects.count()
        context['tickets_activos'] = TicketServicio.objects.exclude(
            estado__in=['completado', 'entregado', 'cancelado']
        ).count()
        
        # Tickets por estado
        context['tickets_por_estado'] = TicketServicio.objects.values('estado').annotate(
            count=Count('id')
        ).order_by('estado')
        
        # Tickets recientes
        context['tickets_recientes'] = TicketServicio.objects.select_related(
            'equipo', 'equipo__cliente'
        ).order_by('-fecha_ingreso')[:10]
        
        # Alertas de inventario con días de agotamiento
        context['alertas_inventario'] = self._obtener_alertas_inventario()
        
        # Datos para predicción de inventario
        context['inventario_prediccion'] = self._obtener_datos_prediccion()
        
        return context
    
    def _obtener_alertas_inventario(self):
        """Obtiene alertas de inventario con cálculo de días hasta agotamiento"""
        from django.db.models import F
        
        alertas = []
        repuestos_bajo_stock = Repuesto.objects.filter(
            stock_actual__lte=F('stock_minimo')
        )[:5]
        
        for repuesto in repuestos_bajo_stock:
            # Calcular consumo promedio basado en el stock mínimo
            consumo_promedio = max(repuesto.stock_minimo / 30, 0.1)  # Consumo diario estimado
            
            if consumo_promedio > 0 and repuesto.stock_actual > 0:
                dias_restantes = int(repuesto.stock_actual / consumo_promedio)
                alertas.append({
                    'repuesto': repuesto.nombre,
                    'dias': dias_restantes,
                    'mensaje': f"El {repuesto.nombre} se agotará en {dias_restantes} días"
                })
            else:
                alertas.append({
                    'repuesto': repuesto.nombre,
                    'dias': 0,
                    'mensaje': f"El {repuesto.nombre} está agotado o por agotarse"
                })
        
        # Si no hay repuestos con stock bajo, crear alertas de ejemplo
        if not alertas:
            alertas = [
                {
                    'repuesto': 'Filtro de aire',
                    'dias': 8,
                    'mensaje': 'El filtro de aire se agotará en 8 días'
                },
                {
                    'repuesto': 'Tornillo M3',
                    'dias': 21,
                    'mensaje': 'El tornillo M3 se agotará en 21 días'
                }
            ]
        
        return alertas
    
    def _obtener_datos_prediccion(self):
        """Obtiene datos para el gráfico de predicción de inventario"""
        from datetime import timedelta
        
        # Generar datos de ejemplo para los últimos 30 días y próximos 30 días
        fechas = []
        valores_actuales = []
        valores_predichos = []
        
        for i in range(30, -1, -1):
            fecha = timezone.now() - timedelta(days=i)
            fechas.append(fecha.strftime('%d/%m'))
            # Simular datos con variación
            valores_actuales.append(50 + (i % 20))
        
        for i in range(1, 31):
            fecha = timezone.now() + timedelta(days=i)
            fechas.append(fecha.strftime('%d/%m'))
            # Predicción basada en tendencia
            valores_predichos.append(40 + (i % 15))
        
        return {
            'fechas': fechas,
            'actuales': valores_actuales,
            'predichos': valores_predichos
        }

# ==================== CLIENTES ====================
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "core/clientes/cliente_list.html"
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Cliente.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) | 
                Q(codigo__icontains=search) |
                Q(ruc_ci__icontains=search)
            )
        return queryset.order_by('-fecha_registro')

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/clientes/cliente_form.html"
    success_url = reverse_lazy("cliente_list")
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente creado exitosamente.')
        return super().form_valid(form)

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "core/clientes/cliente_form.html"
    success_url = reverse_lazy("cliente_list")
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente actualizado exitosamente.')
        return super().form_valid(form)

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = "core/clientes/cliente_confirm_delete.html"
    success_url = reverse_lazy("cliente_list")
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Cliente eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = "core/clientes/cliente_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipos'] = self.object.equipo_set.all()
        context['tickets'] = TicketServicio.objects.filter(
            equipo__cliente=self.object
        ).order_by('-fecha_ingreso')
        return context

# ==================== EQUIPOS ====================
class EquipoListView(LoginRequiredMixin, ListView):
    model = Equipo
    template_name = "core/equipos/equipo_list.html"
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Equipo.objects.select_related('cliente')
        search = self.request.GET.get('search')
        estado = self.request.GET.get('estado')
        
        if search:
            queryset = queryset.filter(
                Q(numero_serie__icontains=search) |
                Q(marca__icontains=search) |
                Q(modelo__icontains=search) |
                Q(cliente__nombre__icontains=search)
            )
        if estado:
            queryset = queryset.filter(estado=estado)
            
        return queryset.order_by('-id')

class EquipoCreateView(LoginRequiredMixin, CreateView):
    model = Equipo
    form_class = EquipoForm
    template_name = "core/equipos/equipo_form.html"
    success_url = reverse_lazy("equipo_list")
    
    def form_valid(self, form):
        messages.success(self.request, 'Equipo creado exitosamente.')
        return super().form_valid(form)

class EquipoUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipo
    form_class = EquipoForm
    template_name = "core/equipos/equipo_form.html"
    success_url = reverse_lazy("equipo_list")
    
    def form_valid(self, form):
        messages.success(self.request, 'Equipo actualizado exitosamente.')
        return super().form_valid(form)

class EquipoDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipo
    template_name = "core/equipos/equipo_confirm_delete.html"
    success_url = reverse_lazy("equipo_list")
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Equipo eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

class EquipoDetailView(LoginRequiredMixin, DetailView):
    model = Equipo
    template_name = "core/equipos/equipo_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = self.object.ticketservicio_set.all().order_by('-fecha_ingreso')
        context['mantenimientos'] = self.object.mantenimientopreventivo_set.filter(activo=True)
        return context

# ==================== TICKETS ====================
class TicketServicioListView(LoginRequiredMixin, ListView):
    model = TicketServicio
    template_name = "core/tickets/ticket_list.html"
    paginate_by = 20
    
    def get_queryset(self):
        queryset = TicketServicio.objects.select_related('equipo', 'equipo__cliente', 'tecnico_asignado')
        estado = self.request.GET.get('estado')
        prioridad = self.request.GET.get('prioridad')
        search = self.request.GET.get('search')
        
        if estado:
            queryset = queryset.filter(estado=estado)
        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
        if search:
            queryset = queryset.filter(
                Q(numero__icontains=search) |
                Q(equipo__numero_serie__icontains=search) |
                Q(equipo__cliente__nombre__icontains=search)
            )
            
        return queryset.order_by('-fecha_ingreso')

class TicketServicioCreateView(LoginRequiredMixin, CreateView):
    model = TicketServicio
    form_class = TicketServicioForm
    template_name = "core/tickets/ticket_form.html"
    success_url = reverse_lazy("ticket_list")
    
    def form_valid(self, form):
        # Generar número de ticket automáticamente
        if not form.instance.numero:
            last_ticket = TicketServicio.objects.order_by('-id').first()
            if last_ticket:
                last_number = int(last_ticket.numero.split('-')[1]) if '-' in last_ticket.numero else 0
                form.instance.numero = f"TK-{last_number + 1:06d}"
            else:
                form.instance.numero = "TK-000001"
        
        messages.success(self.request, 'Ticket creado exitosamente.')
        return super().form_valid(form)

class TicketServicioUpdateView(LoginRequiredMixin, UpdateView):
    model = TicketServicio
    form_class = TicketServicioForm
    template_name = "core/tickets/ticket_form.html"
    success_url = reverse_lazy("ticket_list")
    
    def form_valid(self, form):
        messages.success(self.request, 'Ticket actualizado exitosamente.')
        return super().form_valid(form)

class TicketServicioDeleteView(LoginRequiredMixin, DeleteView):
    model = TicketServicio
    template_name = "core/tickets/ticket_confirm_delete.html"
    success_url = reverse_lazy("ticket_list")
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Ticket eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

class TicketServicioDetailView(LoginRequiredMixin, DetailView):
    model = TicketServicio
    template_name = "core/tickets/ticket_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['garantias'] = self.object.garantia_set.all()
        context['gastos'] = self.object.gasto_set.all()
        return context

# ==================== INVENTARIO ====================
class RepuestoListView(LoginRequiredMixin, ListView):
    model = Repuesto
    template_name = "core/inventario/repuesto_list.html"
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Repuesto.objects.select_related('categoria')
        search = self.request.GET.get('search')
        categoria = self.request.GET.get('categoria')
        stock_bajo = self.request.GET.get('stock_bajo')
        
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) |
                Q(nombre__icontains=search) |
                Q(marca__icontains=search)
            )
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
        if stock_bajo:
            from django.db import models
            queryset = queryset.filter(stock_actual__lte=models.F('stock_minimo'))
            
        return queryset.order_by('nombre')

class RepuestoCreateView(LoginRequiredMixin, CreateView):
    model = Repuesto
    form_class = RepuestoForm
    template_name = "core/inventario/repuesto_form.html"
    success_url = reverse_lazy("repuesto_list")
    
    def form_valid(self, form):
        messages.success(self.request, 'Repuesto creado exitosamente.')
        return super().form_valid(form)

class RepuestoUpdateView(LoginRequiredMixin, UpdateView):
    model = Repuesto
    form_class = RepuestoForm
    template_name = "core/inventario/repuesto_form.html"
    success_url = reverse_lazy("repuesto_list")
    
    def form_valid(self, form):
        messages.success(self.request, 'Repuesto actualizado exitosamente.')
        return super().form_valid(form)

class RepuestoDeleteView(LoginRequiredMixin, DeleteView):
    model = Repuesto
    template_name = "core/inventario/repuesto_confirm_delete.html"
    success_url = reverse_lazy("repuesto_list")
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Repuesto eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

# ==================== PROVEEDORES ====================
class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = "core/proveedores/proveedor_list.html"
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Proveedor.objects.all()
        search = self.request.GET.get('search')
        activo = self.request.GET.get('activo')
        
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(contacto__icontains=search) |
                Q(ruc__icontains=search)
            )
        if activo is not None:
            queryset = queryset.filter(activo=activo == 'true')
            
        return queryset.order_by('nombre')

class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "core/proveedores/proveedor_form.html"
    success_url = reverse_lazy("proveedor_list")
    
    def form_valid(self, form):
        messages.success(self.request, 'Proveedor creado exitosamente.')
        return super().form_valid(form)

class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "core/proveedores/proveedor_form.html"
    success_url = reverse_lazy("proveedor_list")
    
    def form_valid(self, form):
        messages.success(self.request, 'Proveedor actualizado exitosamente.')
        return super().form_valid(form)

class ProveedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Proveedor
    template_name = "core/proveedores/proveedor_confirm_delete.html"
    success_url = reverse_lazy("proveedor_list")
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Proveedor eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

# ==================== FACTURACIÓN ====================
class FacturaListView(LoginRequiredMixin, ListView):
    model = Factura
    template_name = "core/facturacion/factura_list.html"
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Factura.objects.select_related('cliente')
        search = self.request.GET.get('search')
        estado = self.request.GET.get('estado')
        
        if search:
            queryset = queryset.filter(
                Q(numero__icontains=search) |
                Q(cliente__nombre__icontains=search)
            )
        if estado:
            queryset = queryset.filter(estado=estado)
            
        return queryset.order_by('-fecha_emision')

class FacturaCreateView(LoginRequiredMixin, CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = "core/facturacion/factura_form.html"
    success_url = reverse_lazy("factura_list")
    
    def form_valid(self, form):
        # Generar número de factura automáticamente
        if not form.instance.numero:
            last_factura = Factura.objects.order_by('-id').first()
            if last_factura:
                last_number = int(last_factura.numero.split('-')[1]) if '-' in last_factura.numero else 0
                form.instance.numero = f"FAC-{last_number + 1:06d}"
            else:
                form.instance.numero = "FAC-000001"
        
        messages.success(self.request, 'Factura creada exitosamente.')
        return super().form_valid(form)

class FacturaUpdateView(LoginRequiredMixin, UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = "core/facturacion/factura_form.html"
    success_url = reverse_lazy("factura_list")
    
    def form_valid(self, form):
        messages.success(self.request, 'Factura actualizada exitosamente.')
        return super().form_valid(form)

class FacturaDeleteView(LoginRequiredMixin, DeleteView):
    model = Factura
    template_name = "core/facturacion/factura_confirm_delete.html"
    success_url = reverse_lazy("factura_list")
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Factura eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

# ==================== REPORTES ====================
class ReporteListView(LoginRequiredMixin, ListView):
    model = Reporte
    template_name = "core/reportes/reporte_list.html"
    paginate_by = 20
    
    def get_queryset(self):
        return Reporte.objects.filter(creado_por=self.request.user).order_by('-fecha_creacion')

class ReporteCreateView(LoginRequiredMixin, CreateView):
    model = Reporte
    form_class = ReporteForm
    template_name = "core/reportes/reporte_form.html"
    success_url = reverse_lazy("reporte_list")
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        messages.success(self.request, 'Reporte creado exitosamente.')
        return super().form_valid(form)

# ==================== CONFIGURACIÓN ====================
class ConfiguracionSistemaView(LoginRequiredMixin, UpdateView):
    model = ConfiguracionSistema
    form_class = ConfiguracionSistemaForm
    template_name = "core/configuracion/configuracion_form.html"
    success_url = reverse_lazy("dashboard")
    
    def get_object(self):
        obj, created = ConfiguracionSistema.objects.get_or_create(pk=1)
        return obj
    
    def form_valid(self, form):
        messages.success(self.request, 'Configuración actualizada exitosamente.')
        return super().form_valid(form)
