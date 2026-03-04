import pytest
from django.urls import reverse
from ddf import G
from inventory.models import Product

@pytest.mark.django_db
class TestInventoryViews:

    def test_dashboard_with_filtered_data(self, client, create_100_products):
        """Prueba que el dashboard carga con los productos creados por el fixture."""
        url = reverse('dashboard')
        response = client.get(url)
        
        assert response.status_code == 200
        # Verificamos que al menos un producto del fixture aparezca
        assert "ANÁLISIS DE SISTEMA" in response.content.decode()

    def test_export_csv_view(self, client, create_100_products):
        """Verifica que la descarga de CSV responda correctamente."""
        url = reverse('export_csv')
        response = client.get(url)
        
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv'
        assert 'attachment; filename="reporte_inventario.csv"' in response['Content-Disposition']

    def test_export_pdf_view(self, client):
        """Prueba la generación de PDF para un producto específico."""
        product = G(Product, name="PDF Product")
        url = reverse('export_pdf', kwargs={'product_id': product.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/pdf'
        # El contenido de un PDF empieza con %PDF
        assert response.content.startswith(b'%PDF')

