from django.contrib import admin
from .models import Inventory, InventoryGroup, Shop, Invoice, InvoiceItem


admin.site.register((Inventory, InventoryGroup, Shop, Invoice, InvoiceItem))