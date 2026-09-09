from django.contrib import admin
from .models import Catogery

class CategotyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('catogery_name',)}
    list_display = ('catogery_name','slug')

admin.site.register(Catogery,CategotyAdmin)
