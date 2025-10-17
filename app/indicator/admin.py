from django.contrib import admin
from django import forms
from datetime import date
from .models import Indicator
from core.models import Program, SubProgram, Activity


class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = '__all__'
        widgets = {
            'year': forms.Select(choices=[(y, y) for y in range(2000, 2101)]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.initial['year'] = date.today().year


class IndicatorAdmin(admin.ModelAdmin):
    form = IndicatorForm
    change_form_template = "admin/indicator/custom_change_form.html"
    add_form_template = "admin/indicator/custom_add_form.html"
    change_list_template = "admin/indicator/custom_changelist.html"

    def add_view(self, request, form_url='', extra_context=None):
        programs = Program.objects.all().order_by('program_number')
        selected_program = request.GET.get('program')
        year = request.GET.get('year') or date.today().year

        # Default empty lists
        subprograms = []
        activities_by_subprogram = {}
        existing_indicators = {}

        if selected_program:
            subprograms = SubProgram.objects.filter(program_id=selected_program).order_by('subprogram_number')
            for sub in subprograms:
                acts = Activity.objects.filter(subprogram=sub).order_by('activity_number')
                activities_by_subprogram[sub.id] = acts

                for act in acts:
                    try:
                        ind = Indicator.objects.get(year=year, activity=act)
                        existing_indicators[act.id] = {
                            'output_indicator': ind.output_indicator,
                            'target_indicator': ind.target_indicator
                        }
                    except Indicator.DoesNotExist:
                        existing_indicators[act.id] = {
                            'output_indicator': '',
                            'target_indicator': ''
                        }

        if request.method == "POST":
            # Iterate over submitted activity IDs
            for key in request.POST:
                if key.startswith("output_indicator_"):
                    act_id = key.replace("output_indicator_", "")
                    try:
                        act = Activity.objects.get(id=act_id)
                        output_value = request.POST.get(f"output_indicator_{act_id}", "")
                        target_value = request.POST.get(f"target_indicator_{act_id}", "")

                        Indicator.objects.create(
                            year=year,
                            program=act.subprogram.program,
                            subprogram=act.subprogram,
                            activity=act,
                            output_indicator=output_value,
                            target_indicator=target_value,
                        )
                    except Activity.DoesNotExist:
                        continue

            extra_context = extra_context or {}
            extra_context["saved"] = True
            

        extra_context = extra_context or {}
        extra_context.update({
            "year": year,
            "programs": programs,
            "selected_program": selected_program,
            "subprograms": subprograms,
            "activities_by_subprogram": activities_by_subprogram,
        })

        return super().add_view(request, form_url, extra_context=extra_context)
    


    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Get all indicators and group by year → program
        all_indicators = Indicator.objects.select_related('program').order_by('year', 'program__program_number')

        saved_structure = {}
        for ind in all_indicators:
            saved_structure.setdefault(ind.year, set()).add(ind.program)

        extra_context['saved_structure'] = saved_structure

        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Indicator, IndicatorAdmin)
