from django.contrib import admin

from app.models import ServiceCategory, Staff

# Register your models here.
admin.site.site_header = 'Liberator Administration'
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

admin.site.register(Staff)

