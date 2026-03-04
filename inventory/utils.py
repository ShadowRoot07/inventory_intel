import matplotlib
matplotlib.use('Agg') # Backend sin GUI para servidores (Vercel/Render)
import matplotlib.pyplot as plt
import io
from django.core.files.base import ContentFile
from datetime import timedelta
from django.utils import timezone

def generate_inventory_chart(product):
    # 1. Obtener movimientos de los últimos 30 días
    last_month = timezone.now() - timedelta(days=30)
    movements = product.movements.filter(date__gte=last_month).order_by('date')
    
    # 2. Calcular la evolución del stock
    dates = [m.date for m in movements]
    # Calculamos el stock acumulado paso a paso
    stock_evolution = []
    current_val = product.stock_actual # Esto es simplificado, idealmente restas hacia atrás
    
    # Lógica de línea de tiempo
    values = [m.quantity for m in movements]
    cumulative_stock = []
    temp_stock = 0
    for val in values:
        temp_stock += val
        cumulative_stock.append(temp_stock)

    # 3. Crear la gráfica con Matplotlib
    plt.figure(figsize=(8, 4))
    plt.plot(dates, cumulative_stock, marker='o', linestyle='-', color='#10b981') # Color Emerald-ish
    plt.title(f"Evolución de Stock: {product.name}", fontsize=12)
    plt.xlabel("Fecha")
    plt.ylabel("Unidades")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # 4. Guardar en memoria y retornar como archivo de Django
    f = io.BytesIO()
    plt.savefig(f, format='png')
    plt.close() # Limpiar memoria de Matplotlib
    
    return ContentFile(f.getvalue(), name=f"{product.name}_chart.png")

