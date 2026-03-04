from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Product, AutomaticReport 
from .analytics import InventoryAnalytics
from .exporters import InventoryExporter


def dashboard(request):
    # 1. Obtener todos los productos base
    products = Product.objects.all()

    # 2. Capturar filtros desde la URL (?categoria=...&estado=...)
    category_filter = request.GET.get('category')
    stock_status = request.GET.get('status')

    # 3. Aplicar lógica de filtrado
    if category_filter:
        products = products.filter(category__icontains=category_filter)
    
    if stock_status == 'critico':
        products = products.filter(stock_actual__lt=10)
    elif stock_status == 'advertencia':
        products = products.filter(stock_actual__gte=10, stock_actual__lt=25)

    # Lógica del primer producto para la gráfica (el primero que cumpla el filtro)
    first_product = products.first()
    metrics = None
    chart_url = None
    product_id = None

    if first_product:
        product_id = first_product.id
        metrics = InventoryAnalytics.calculate_metrics(first_product)
        
        # Generar reporte diario para el producto filtrado
        report_name = f"Reporte - {first_product.name}"
        report, created = AutomaticReport.objects.get_or_create(
            name=report_name,
            created_at__date=timezone.now().date(),
            defaults={'data_json': metrics}
        )

        if created or not report.chart_png:
            chart_file = InventoryAnalytics.get_stock_timeline(first_product)
            report.chart_png.save(chart_file.name, chart_file)
            report.save()

        chart_url = report.chart_png.url

    # Enviamos las categorías únicas para el dropdown del filtro
    categories = Product.objects.values_list('category', flat=True).distinct()

    return render(request, 'inventory/dashboard.html', {
        'products': products,
        'products_count': products.count(),
        'metrics': metrics,
        'chart_url': chart_url,
        'product_name': first_product.name if first_product else "N/A",
        'product_id': product_id,
        'categories': categories,
    })


def export_products_csv(request):
    products = Product.objects.all()
    return InventoryExporter.to_csv(products)


def export_product_pdf(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    metrics = InventoryAnalytics.calculate_metrics(product)
    return InventoryExporter.to_pdf(product, metrics)

