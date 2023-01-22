from django.contrib import admin

from order.models import Order, Establishment, OrderItem, Product, Delivery


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_type', 'created_at', 'modified_at', 'total', 'paid']
    list_filter = ['order_type']


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'service_price', 'delivery_price']
    list_filter = ['name']
    search_fields = ['name', 'description']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'amount']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'cafe']
    list_filter = ['cafe']
    search_fields = ['name', 'cafe']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'phone', 'description']
    list_filter = ['phone']
    search_fields = ['address', 'description']

