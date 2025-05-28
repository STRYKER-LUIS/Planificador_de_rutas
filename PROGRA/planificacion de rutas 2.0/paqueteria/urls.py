from django.urls import path
from . import views

urlpatterns = [
    path('', views.InicioView.as_view(), name='inicio'),
    path('realizar-envio/', views.RealizarEnvioView.as_view(), name='realizar_envio'),
    path('historial-rutas/', views.HistorialRutasView.as_view(), name='historial_rutas'),
    path('detalle-ruta/<int:pk>/', views.DetalleRutaView.as_view(), name='detalle_ruta'),
] 