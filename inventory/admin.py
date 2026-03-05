from django.contrib import admin
from .models import Product, InventoryMovement, AutomaticReport

admin.site.register(Product)
admin.site.register(InventoryMovement)
admin.site.register(AutomaticReport) # Aunque es editable=False, podrás verlo aquí

