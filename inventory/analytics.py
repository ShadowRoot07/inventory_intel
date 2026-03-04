import matplotlib
matplotlib.use('Agg')  # Indispensable para Vercel/Render (No GUI)
import matplotlib.pyplot as plt
import io
import json
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import timedelta
from .models import InventoryMovement

class InventoryAnalytics:
    @staticmethod
    def get_stock_timeline(product):
        """Genera una línea de tiempo del stock de los últimos 30 días."""
        days_ago = timezone.now() - timedelta(days=30)
        movements = InventoryMovement.objects.filter(
            product=product, 
            date__gte=days_ago
        ).order_by('date')

        # Algoritmo de reconstrucción de línea de tiempo
        dates = []
        stock_values = []
        current_stock = product.stock_actual

        # Retrocedemos en el tiempo para ver la evolución
        # (Ideal para el gráfico de línea que pediste)
        temp_stock = current_stock
        for m in reversed(movements):
            dates.append(m.date)
            stock_values.append(temp_stock)
            temp_stock -= m.quantity  # Restamos el movimiento para ver el pasado

        # Invertimos para que el gráfico vaya de pasado a presente
        dates.reverse()
        stock_values.reverse()

        # Configuración de Matplotlib estilo "Tech"
        plt.figure(figsize=(10, 5), facecolor='#f8fafc')
        plt.plot(dates, stock_values, color='#10b981', linewidth=2, marker='o', markersize=4)
        plt.fill_between(dates, stock_values, color='#10b981', alpha=0.1)
        
        plt.title(f"Línea de Tiempo: {product.name}", fontsize=14, fontweight='bold', color='#0f172a')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()

        # Guardar en buffer de memoria
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        
        return ContentFile(buffer.getvalue(), name=f"report_{product.id}_{timezone.now().date()}.png")

    @staticmethod
    def calculate_metrics(product):
        """Algoritmo para reporte automático en JSON."""
        movements = product.movements.all()
        entradas = sum(m.quantity for m in movements if m.type == 'IN')
        salidas = abs(sum(m.quantity for m in movements if m.type == 'OUT'))
        
        # Análisis automático: ¿Necesitamos reponer?
        status = "Saludable"
        if product.stock_actual < 10:
            status = "Crítico: Reposición Inmediata"
        elif product.stock_actual < 25:
            status = "Advertencia: Stock Bajo"

        metrics = {
            "total_entradas": entradas,
            "total_salidas": salidas,
            "balance": entradas - salidas,
            "estado_alerta": status,
            "fecha_analisis": timezone.now().strftime("%Y-%m-%d %H:%M")
        }
        return metrics

