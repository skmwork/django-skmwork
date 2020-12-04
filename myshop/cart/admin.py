from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_key','created', 'updated', 'user']
    list_filter = ['created', 'updated']
    inlines = [CartItemInline]


admin.site.register(Cart, CartAdmin)