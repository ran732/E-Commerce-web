from django.contrib import admin

from . models import Product,Variation

class productAdmin(admin.ModelAdmin):
    
    list_display = ('product_name','price','stocks','category','created_date','modified_date','is_available')
    
    prepopulated_fields = {'slug':('product_name',),}


class VariationAdmin(admin.ModelAdmin):
    
    list_display = ('product','variation_value','is_active','created_date')
    list_editable = ('is_active',)
    list_filter =('variation_category','product','is_active')
        

    
    
admin.site.register(Product,productAdmin)
admin.site.register(Variation,VariationAdmin)
