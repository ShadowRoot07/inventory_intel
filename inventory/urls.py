from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('export/csv/', views.export_products_csv, name='export_csv'),
    path('export/pdf/<int:product_id>/', views.export_product_pdf, name='export_pdf'),
]

