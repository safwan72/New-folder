from django.contrib import admin
from .models import ActiveAdminModel, ActiveCompany
# Register your models here.


class ActiveModelAdmin(admin.ModelAdmin):
    list_display = (
            'app_level', 'model_name',
            'title', 'base_url', 'is_active'
        )
    readonly_fields = (
            'app_level', 'model_name', 'base_url'
        )


admin.site.register(ActiveAdminModel, ActiveModelAdmin)


class ActiveCompanyAdmin(admin.ModelAdmin):
    list_display = (
            'entry_name', 'email', 'phone', 'license_key',
            'domain', 'is_active', 'create_date', 'update_date'
        )


admin.site.register(ActiveCompany, ActiveCompanyAdmin)
