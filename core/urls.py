from django.urls import path
from . import views

urlpatterns = [
    # DASHBOARD
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # CLIENTES
    path('clientes/', views.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='cliente_detail'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_edit'),
    path('clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_delete'),

    # EQUIPOS
    path('equipos/', views.EquipoListView.as_view(), name='equipo_list'),
    path('equipos/nuevo/', views.EquipoCreateView.as_view(), name='equipo_create'),
    path('equipos/<int:pk>/', views.EquipoDetailView.as_view(), name='equipo_detail'),
    path('equipos/<int:pk>/editar/', views.EquipoUpdateView.as_view(), name='equipo_edit'),
    path('equipos/<int:pk>/eliminar/', views.EquipoDeleteView.as_view(), name='equipo_delete'),

    # TICKETS
    path('tickets/', views.TicketServicioListView.as_view(), name='ticket_list'),
    path('tickets/nuevo/', views.TicketServicioCreateView.as_view(), name='ticket_create'),
    path('tickets/<int:pk>/', views.TicketServicioDetailView.as_view(), name='ticket_detail'),
    path('tickets/<int:pk>/editar/', views.TicketServicioUpdateView.as_view(), name='ticket_edit'),
    path('tickets/<int:pk>/eliminar/', views.TicketServicioDeleteView.as_view(), name='ticket_delete'),

    # INVENTARIO
    path('inventario/repuestos/', views.RepuestoListView.as_view(), name='repuesto_list'),
    path('inventario/repuestos/nuevo/', views.RepuestoCreateView.as_view(), name='repuesto_create'),
    path('inventario/repuestos/<int:pk>/editar/', views.RepuestoUpdateView.as_view(), name='repuesto_edit'),
    path('inventario/repuestos/<int:pk>/eliminar/', views.RepuestoDeleteView.as_view(), name='repuesto_delete'),

    # PROVEEDORES
    path('proveedores/', views.ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/nuevo/', views.ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedores/<int:pk>/editar/', views.ProveedorUpdateView.as_view(), name='proveedor_edit'),
    path('proveedores/<int:pk>/eliminar/', views.ProveedorDeleteView.as_view(), name='proveedor_delete'),

    # FACTURACIÓN
    path('facturacion/', views.FacturaListView.as_view(), name='factura_list'),
    path('facturacion/nueva/', views.FacturaCreateView.as_view(), name='factura_create'),
    path('facturacion/<int:pk>/editar/', views.FacturaUpdateView.as_view(), name='factura_edit'),
    path('facturacion/<int:pk>/eliminar/', views.FacturaDeleteView.as_view(), name='factura_delete'),

    # REPORTES
    path('reportes/', views.ReporteListView.as_view(), name='reporte_list'),
    path('reportes/nuevo/', views.ReporteCreateView.as_view(), name='reporte_create'),

    # CONFIGURACIÓN
    path('configuracion/', views.ConfiguracionSistemaView.as_view(), name='configuracion'),
]
