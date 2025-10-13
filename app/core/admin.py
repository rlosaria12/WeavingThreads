from django.contrib import admin
from core.models import Program, SubProgram, Activity

class ProgramAdmin(admin.ModelAdmin):
    #list_display = ('program_number', 'program')
    ordering = ('program_number',)

class SubProgramAdmin(admin.ModelAdmin):
    list_display = ('formatted_subprogram',)
    list_filter = ('program',)
    ordering = ('program__program_number', 'subprogram_number')

    def formatted_subprogram(self, obj):
        return f"{obj.program.program_number}.{obj.subprogram_number} {obj.subprogram}"
    formatted_subprogram.short_description = "Sub-Programs"

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('formatted_activity',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Proper ordering by related fields
        return qs.select_related('subprogram', 'subprogram__program').order_by(
            'subprogram__program__program_number',
            'subprogram__subprogram_number',
            'activity_number'
        )

    def formatted_activity(self, obj):
        return f"{obj.subprogram.program.program_number}.{obj.subprogram.subprogram_number}.{obj.activity_number} {obj.activity}"
    formatted_activity.short_description = "Activities"


# Register models
admin.site.register(Program, ProgramAdmin)
admin.site.register(SubProgram, SubProgramAdmin)
admin.site.register(Activity, ActivityAdmin)
