from django.contrib import admin
from .models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Fields displayed in the list view
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate the slug based on name
    search_fields = ('name',)  # Add search functionality based on the category name
    list_filter = ('name',)  # Filtering options based on name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'is_featured', 'created_at')
    list_editable = ('price', 'stock', 'is_active', 'is_featured')  # Allow editing these fields directly in the list view
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate the slug based on name
    search_fields = ('name', 'description')  # Add search functionality based on product name and description
    list_filter = ('category', 'is_active', 'is_featured', 'created_at')  # Filter options for better admin navigation
    readonly_fields = ('created_at', 'updated_at')  # Display these fields as read-only

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description', 'image')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'stock')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Related Products', {
            'fields': ('related_products',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    filter_horizontal = ('related_products',)  # Display a horizontal filter widget for related products
