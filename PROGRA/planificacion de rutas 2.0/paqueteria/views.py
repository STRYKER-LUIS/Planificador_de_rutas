from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from .models import Envio, HistorialRuta
from .utils import crear_grafo_guatemala
import json

# Create your views here.

class InicioView(TemplateView):
    template_name = 'paqueteria/inicio.html'

class RealizarEnvioView(TemplateView):
    template_name = 'paqueteria/realizar_envio.html'

    def post(self, request, *args, **kwargs):
        try:
            # Obtener datos del formulario
            remitente = request.POST.get('remitente')
            num_paquetes = int(request.POST.get('num_paquetes'))
            peso_total = float(request.POST.get('peso_total'))
            punto_inicio = request.POST.get('punto_inicio')
            punto_fin = request.POST.get('punto_fin')
            coordenadas_inicio = request.POST.get('coordenadas_inicio')
            coordenadas_fin = request.POST.get('coordenadas_fin')

            # Crear nuevo envío
            envio = Envio.objects.create(
                remitente=remitente,
                num_paquetes=num_paquetes,
                peso_total=peso_total,
                punto_inicio=punto_inicio,
                punto_fin=punto_fin,
                coordenadas_inicio=coordenadas_inicio,
                coordenadas_fin=coordenadas_fin
            )

            # Calcular ruta optimizada usando Dijkstra
            grafo = crear_grafo_guatemala()
            inicio_coords = json.loads(coordenadas_inicio)
            fin_coords = json.loads(coordenadas_fin)
            
            # Encontrar los puntos más cercanos en el grafo
            inicio = min(grafo.coordenadas.items(), 
                        key=lambda x: grafo.calcular_distancia(inicio_coords, x[1]))[0]
            fin = min(grafo.coordenadas.items(), 
                     key=lambda x: grafo.calcular_distancia(fin_coords, x[1]))[0]
            
            # Calcular ruta optimizada
            ruta, distancia = grafo.dijkstra(inicio, fin)
            
            if ruta:
                # Obtener coordenadas de la ruta
                coordenadas_ruta = grafo.obtener_coordenadas_ruta(ruta)
                
                # Agregar punto inicial y final exactos
                coordenadas_ruta.insert(0, inicio_coords)
                coordenadas_ruta.append(fin_coords)
                
                # Guardar ruta optimizada
                envio.ruta_optimizada = {
                    'ruta': ruta,
                    'coordenadas': coordenadas_ruta,
                    'distancia': distancia,
                    'tiempo_estimado': distancia / 50  # Estimación de tiempo (50 km/h promedio)
                }
                envio.save()
                
                messages.success(request, '¡Envío creado exitosamente con ruta optimizada!')
            else:
                messages.warning(request, 'No se pudo encontrar una ruta optimizada. Se usará la ruta directa.')

            return redirect('historial_rutas')

        except Exception as e:
            messages.error(request, f'Error al crear el envío: {str(e)}')
            return redirect('realizar_envio')

class HistorialRutasView(ListView):
    model = Envio
    template_name = 'paqueteria/historial_rutas.html'
    context_object_name = 'envios'
    ordering = ['-fecha_creacion']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Historial de Envíos'
        return context

class DetalleRutaView(DetailView):
    model = Envio
    template_name = 'paqueteria/detalle_ruta.html'
    context_object_name = 'envio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle de Envío'
        return context
