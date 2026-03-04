import json
from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=100)
    stock_actual = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self, *args, **kwargs):
        if self.pk:
            original = Product.objects.get(pk=self.pk)
            if original.name != self.name:
                raise ValidationError("El nombre del producto es inmutable.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class InventoryMovement(models.Model):
    TYPE_CHOICES = [('IN', 'Entrada'), ('OUT', 'Salida')]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    quantity = models.IntegerField() # Positivo para entrada, negativo para salida
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.type} - {self.product.name} ({self.quantity})"

class AutomaticReport(models.Model):
    # El nombre se genera automáticamente o se pide una vez, luego es inmutable
    name = models.CharField(max_length=255, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    data_json = models.JSONField() # Aquí guardaremos los cálculos del reporte
    chart_png = models.ImageField(upload_to='reports/charts/', null=True, blank=True)

    def __str__(self):
        return f"Reporte {self.name} - {self.created_at.strftime('%Y-%m-%d')}"

