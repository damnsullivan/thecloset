from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'total_price', 'created_at', 'updated_at']
    list_filter = ['user', 'product']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['created_at', 'updated_at']

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'
