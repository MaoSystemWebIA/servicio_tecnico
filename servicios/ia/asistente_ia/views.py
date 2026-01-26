import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import models
from core.models import TicketServicio, Cliente, Equipo, Repuesto
from .models import Conversacion


@csrf_exempt
@login_required
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            mensaje = data.get("mensaje", "").strip()
            
            if not mensaje:
                return JsonResponse({"error": "Mensaje vacío"}, status=400)
            
            # Procesar mensaje con lógica inteligente
            respuesta = procesar_mensaje_ia(mensaje, request.user)
            
            # Guardar conversación
            Conversacion.objects.create(
                mensaje_usuario=mensaje,
                respuesta_ia=respuesta
            )
            
            return JsonResponse({
                "mensaje_usuario": mensaje,
                "respuesta_ia": respuesta
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Solo POST permitido"}, status=405)


def procesar_mensaje_ia(mensaje, usuario):
    """Procesa el mensaje y genera una respuesta inteligente"""
    mensaje_lower = mensaje.lower()
    
    # Detectar tickets retrasados
    if any(palabra in mensaje_lower for palabra in ['retrasado', 'retraso', 'atrasado', 'tardanza', 'retrasados']):
        tickets_retrasados = TicketServicio.objects.filter(
            fecha_prometida__lt=timezone.now(),
            estado__in=['recibido', 'diagnostico', 'reparacion', 'espera_repuestos']
        ).order_by('fecha_prometida')[:5]
        
        if tickets_retrasados.exists():
            respuesta = f"Hay {tickets_retrasados.count()} ticket(s) retrasado(s):\n\n"
            for ticket in tickets_retrasados:
                dias_retraso = (timezone.now() - ticket.fecha_prometida).days if ticket.fecha_prometida else 0
                respuesta += f"• {ticket.numero} ({ticket.equipo.cliente.nombre}): {dias_retraso} días de retraso\n"
            respuesta += "\n¿Necesitas más información?"
        else:
            respuesta = "No hay tickets retrasados en este momento. Todos los tickets están al día."
    
    # Detectar consulta de ticket específico
    elif any(palabra in mensaje_lower for palabra in ['ticket', 'tkt', 'tkt-']):
        # Buscar número de ticket en el mensaje
        numeros = re.findall(r'tkt-?\d+', mensaje_lower)
        if not numeros:
            numeros = re.findall(r'\d+', mensaje)
        
        if numeros:
            try:
                # Buscar ticket por número
                numero_buscar = numeros[0].replace('tkt-', '').replace('tkt', '')
                ticket = TicketServicio.objects.filter(
                    numero__icontains=numero_buscar
                ).first()
                
                if ticket:
                    respuesta = f"📋 **Ticket {ticket.numero}**\n\n"
                    respuesta += f"👤 Cliente: {ticket.equipo.cliente.nombre}\n"
                    respuesta += f"💻 Equipo: {ticket.equipo.marca} {ticket.equipo.modelo}\n"
                    respuesta += f"📊 Estado: {ticket.get_estado_display()}\n"
                    respuesta += f"🔧 Problema: {ticket.problema_reportado[:100]}...\n"
                    if ticket.fecha_prometida:
                        respuesta += f"📅 Fecha prometida: {ticket.fecha_prometida.strftime('%d/%m/%Y')}\n"
                    respuesta += "\n¿Necesitas más información?"
                else:
                    respuesta = f"No se encontró el ticket {numeros[0]}. ¿Puedes verificar el número?"
            except Exception as e:
                respuesta = f"Error al buscar el ticket: {str(e)}"
        else:
            respuesta = "¿Sobre qué ticket te gustaría información? Puedes mencionar el número (ej: TKT-001)."
    
    # Detectar consulta de cliente
    elif any(palabra in mensaje_lower for palabra in ['cliente', 'clientes', 'cuántos clientes']):
        total = Cliente.objects.count()
        respuesta = f"Actualmente hay {total} cliente(s) registrado(s). "
        respuesta += "¿Quieres información sobre algún cliente específico?"
    
    # Detectar consulta de equipos
    elif any(palabra in mensaje_lower for palabra in ['equipo', 'equipos', 'cuántos equipos']):
        total = Equipo.objects.count()
        respuesta = f"Hay {total} equipo(s) registrado(s). "
        respuesta += "¿Necesitas información sobre algún equipo en particular?"
    
    # Detectar consulta de inventario
    elif any(palabra in mensaje_lower for palabra in ['inventario', 'stock', 'repuestos']):
        total_repuestos = Repuesto.objects.count()
        stock_bajo = Repuesto.objects.filter(stock_actual__lte=models.F('stock_minimo')).count()
        respuesta = f"📦 Inventario:\n"
        respuesta += f"• Total de repuestos: {total_repuestos}\n"
        respuesta += f"• Con stock bajo: {stock_bajo}\n"
        respuesta += "\n¿Quieres más detalles sobre algún repuesto específico?"
    
    # Respuesta por defecto
    else:
        respuesta = f"Entiendo tu consulta: '{mensaje}'. "
        respuesta += "Puedo ayudarte con información sobre:\n"
        respuesta += "• Tickets retrasados\n"
        respuesta += "• Información de tickets específicos\n"
        respuesta += "• Clientes y equipos\n"
        respuesta += "• Inventario y stock\n\n"
        respuesta += "¿Sobre qué te gustaría saber más?"
    
    return respuesta


@csrf_exempt
@login_required
def diagnostico_inteligente(request):
    """Genera diagnóstico inteligente basado en síntomas"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            problema = data.get("problema", "")
            
            if not problema:
                return JsonResponse({"error": "Problema no especificado"}, status=400)
            
            diagnostico = generar_diagnostico(problema)
            
            return JsonResponse(diagnostico)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Solo POST permitido"}, status=405)


def generar_diagnostico(problema):
    """Genera diagnóstico con porcentajes de probabilidad"""
    problema_lower = problema.lower()
    
    diagnosticos = []
    
    # Detectar sobrecalentamiento
    if any(palabra in problema_lower for palabra in ['apaga', 'caliente', 'sobrecalentamiento', 'temperatura', 'calor', 'se apaga']):
        diagnosticos.append({
            "causa": "Sobrecalentamiento",
            "probabilidad": 82,
            "descripcion": "El equipo se apaga debido a sobrecalentamiento. Verificar ventiladores y pasta térmica."
        })
    
    # Detectar daño en disco duro
    if any(palabra in problema_lower for palabra in ['lento', 'lenta', 'disco', 'hdd', 'ssd', 'almacenamiento', 'muy lenta']):
        diagnosticos.append({
            "causa": "Daño en disco duro",
            "probabilidad": 45,
            "descripcion": "Posible daño en el disco duro. Verificar con herramientas de diagnóstico."
        })
    
    # Detectar problemas de RAM
    if any(palabra in problema_lower for palabra in ['lento', 'lenta', 'memoria', 'ram', 'muy lenta']):
        if not any(d['causa'] == 'RAM' for d in diagnosticos):
            diagnosticos.append({
                "causa": "RAM",
                "probabilidad": 29,
                "descripcion": "Posible problema con la memoria RAM. Ejecutar diagnóstico de memoria."
            })
    
    # Detectar problemas de batería
    if any(palabra in problema_lower for palabra in ['batería', 'bateria', 'no enciende', 'no carga']):
        diagnosticos.append({
            "causa": "Batería",
            "probabilidad": 65,
            "descripcion": "Problema con la batería. Verificar estado y capacidad."
        })
    
    # Si no hay coincidencias, dar diagnósticos genéricos
    if not diagnosticos:
        diagnosticos = [
            {
                "causa": "Diagnóstico general",
                "probabilidad": 50,
                "descripcion": "Se requiere diagnóstico más detallado para determinar la causa exacta."
            }
        ]
    
    # Ordenar por probabilidad
    diagnosticos.sort(key=lambda x: x['probabilidad'], reverse=True)
    
    return {
        "problema": problema,
        "diagnosticos": diagnosticos[:3]  # Top 3
    }
