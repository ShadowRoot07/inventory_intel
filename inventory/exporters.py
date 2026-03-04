import csv
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class InventoryExporter:
    @staticmethod
    def to_csv(queryset):
        """Genera un archivo CSV con los datos del queryset."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte_inventario.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Producto', 'Categoría', 'Stock', 'Precio', 'Fecha Creación'])
        
        for p in queryset:
            writer.writerow([p.id, p.name, p.category, p.stock_actual, p.price, p.created_at])
            
        return response

    @staticmethod
    def to_pdf(product, metrics):
        """Genera un PDF profesional con el análisis del producto."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Título
        elements.append(Paragraph(f"Reporte de Inteligencia: {product.name}", styles['Title']))
        elements.append(Paragraph(f"Análisis generado por ShadowRoot-Agro System", styles['Normal']))
        elements.append(Paragraph("<br/><br/>", styles['Normal']))

        # Tabla de Datos
        data = [
            ['Métrica', 'Valor'],
            ['Stock Actual', f"{product.stock_actual} unidades"],
            ['Precio Unitario', f"${product.price}"],
            ['Total Entradas', metrics.get('total_entradas', 0)],
            ['Total Salidas', metrics.get('total_salidas', 0)],
            ['Estado de Alerta', metrics.get('estado_alerta', 'N/A')],
        ]

        t = Table(data, colWidths=[150, 250])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkslategray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(t)

        # Finalizar PDF
        doc.build(elements)
        buffer.seek(0)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte_{product.id}.pdf"'
        response.write(buffer.getvalue())
        return response

