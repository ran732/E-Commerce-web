from django.contrib import admin

from . models import Product

class productAdmin(admin.ModelAdmin):
    
    list_display = ('product_name','price','stocks','category','created_date','modified_date','is_available')
    
    prepopulated_fields = {'slug':('product_name',),}

admin.site.register(Product,productAdmin)
