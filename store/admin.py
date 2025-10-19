from django.contrib import admin
# store/admin.py
from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price_at_purchase')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'total')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)
    list_filter = ('status',)


# Register your models here.
