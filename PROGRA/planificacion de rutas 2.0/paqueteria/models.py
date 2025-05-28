from django.db import models
from django.contrib.auth.models import User

class Envio(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado')
    ]

    remitente = models.CharField(max_length=100, verbose_name="Remitente")
    num_paquetes = models.IntegerField(verbose_name="Número de Paquetes")
    peso_total = models.FloatField(verbose_name="Peso Total (lbs)")
    costo = models.FloatField(verbose_name="Costo Total")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    punto_inicio = models.CharField(max_length=200, verbose_name="Punto de Inicio")
    punto_fin = models.CharField(max_length=200, verbose_name="Punto de Destino")
    coordenadas_inicio = models.CharField(max_length=100, verbose_name="Coordenadas de Inicio")
    coordenadas_fin = models.CharField(max_length=100, verbose_name="Coordenadas de Destino")
    ruta_optimizada = models.JSONField(null=True, blank=True, verbose_name="Ruta Optimizada")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name="Estado")

    def calcular_costo(self):
        return self.peso_total * 55  # $55 por libra

    def save(self, *args, **kwargs):
        self.costo = self.calcular_costo()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Envío de {self.remitente} - {self.fecha_creacion.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"
        ordering = ['-fecha_creacion']

class HistorialRuta(models.Model):
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, verbose_name="Envío")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    ruta_completa = models.JSONField(verbose_name="Ruta Completa")

    def __str__(self):
        return f"Ruta para envío {self.envio.id} - {self.fecha_creacion.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Historial de Ruta"
        verbose_name_plural = "Historial de Rutas"
        ordering = ['-fecha_creacion']
