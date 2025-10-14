from django.contrib import admin
from .models import EndUser

class EndUserAdmin(admin.ModelAdmin):
    list_display = ('office_name', 'office_type')  # match model fields
    list_filter = ('office_type',)

admin.site.register(EndUser, EndUserAdmin)