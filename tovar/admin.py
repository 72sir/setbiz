from django.contrib import admin
from .models import Product, Attribute, OrderPaymentProduct, MatrixProduct, FotoTovar


# Register your models here.

class FotoTovarInline(admin.TabularInline):
    model = FotoTovar
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'company', 'type', 'model')
    search_fields = ['name']
    inlines = [FotoTovarInline]


admin.site.register(Product, ProductAdmin)


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'destination', 'company', 'type', 'model')
    fields = ('name', 'destination', 'company', 'type', 'model', 'parent')


admin.site.register(Attribute, AttributeAdmin)


class OrderPaymentProductAdmin(admin.ModelAdmin):
    list_display = ('userPayment', 'product')


admin.site.register(OrderPaymentProduct, OrderPaymentProductAdmin)

admin.site.register(MatrixProduct)

