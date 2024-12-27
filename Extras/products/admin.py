from django.contrib import admin
from .models import Category, Product, Size

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_display_name')

    def get_display_name(self, obj):
        return obj.get_name_display()
    get_display_name.short_description = 'Display Name'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created', 'updated')
    list_filter = ('available', 'created', 'updated', 'category', 'sizes')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description', 'brand')
    ordering = ('-created',)
    filter_horizontal = ('sizes',)
    readonly_fields = ('created', 'updated')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description', 'brand', 'price', 'image')
        }),
        ('Availability', {
            'fields': ('stock', 'available')
        }),
        ('Attributes', {
            'fields': ('sizes', 'color', 'gender', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )

    def get_sizes(self, obj):
        return ", ".join([size.name for size in obj.sizes.all()])
    get_sizes.short_description = 'Sizes'