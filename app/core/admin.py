from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from core.models import Program, SubProgram, Activity, SubActivity

class ProgramAdmin(admin.ModelAdmin):
    #list_display = ('program_number', 'program')
    ordering = ('program_number',)

class SubProgramAdmin(admin.ModelAdmin):
    list_display = ('program_name', 'formatted_subprogram',)
    list_display_links = ('formatted_subprogram',)  # only Sub-Program column makes the row clickable
    list_filter = ('program',)
    ordering = ('program__program_number', 'subprogram_number')

    def program_name(self, obj):
        return f"{obj.program.program_number}. {obj.program.program}"
    program_name.short_description = "Program"

    def formatted_subprogram(self, obj):
        return f"{obj.program.program_number}.{obj.subprogram_number} {obj.subprogram}"
    formatted_subprogram.short_description = "Sub-Program"

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('formatted_subprogram', 'formatted_activity')
    list_display_links = ('formatted_activity',)  # make only Activity clickable

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('subprogram', 'subprogram__program').order_by(
            'subprogram__program__program_number',
            'subprogram__subprogram_number',
            'activity_number'
        )

    def formatted_subprogram(self, obj):
        return f"{obj.subprogram.program.program_number}.{obj.subprogram.subprogram_number} {obj.subprogram.subprogram}"
    formatted_subprogram.short_description = "Sub-Program"

    def formatted_activity(self, obj):
        return f"{obj.subprogram.program.program_number}.{obj.subprogram.subprogram_number}.{obj.activity_number} {obj.activity}"
    formatted_activity.short_description = "Activity"

class SubActivityAdmin(admin.ModelAdmin):
    list_display = ('formatted_activity', 'formatted_subactivity')
    list_display_links = ('formatted_subactivity',)  # make both clickable

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'activity',
            'activity__subprogram',
            'activity__subprogram__program'
        )

    def formatted_activity(self, obj):
        return f"{obj.activity.subprogram.program.program_number}." \
               f"{obj.activity.subprogram.subprogram_number}." \
               f"{obj.activity.activity_number} {obj.activity.activity}"
    formatted_activity.short_description = "Activity"

    def formatted_subactivity(self, obj):
        return f"{obj.activity.subprogram.program.program_number}." \
               f"{obj.activity.subprogram.subprogram_number}." \
               f"{obj.activity.activity_number}." \
               f"{obj.subactivity_number} {obj.subactivity}"
    formatted_subactivity.short_description = "Sub-Activity"


    
# Register models
admin.site.register(Program, ProgramAdmin)
admin.site.register(SubProgram, SubProgramAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(SubActivity, SubActivityAdmin)
