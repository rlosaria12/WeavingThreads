from django.shortcuts import render
from .models import Indicator
from core.models import Program

def indicator_list_view(request):
    year = request.GET.get('year')  # optional filter
    indicators_by_year = {}

    indicators_qs = Indicator.objects.all()
    if year:
        indicators_qs = indicators_qs.filter(year=year)

    programs = Program.objects.prefetch_related(
        'subprogram_set__activity_set__indicator_set'
    )

    for program in programs:
        subprograms_dict = {}
        for sub in program.subprogram_set.all():
            activities_dict = {}
            for act in sub.activity_set.all():
                indicators = act.indicator_set.filter(year=year) if year else act.indicator_set.all()
                if indicators.exists():
                    activities_dict[act] = indicators
            if activities_dict:
                subprograms_dict[sub] = activities_dict
        if subprograms_dict:
            indicators_by_year[program] = subprograms_dict

    context = {
        'year': year,
        'indicators_by_year': indicators_by_year,
    }
    return render(request, 'indicator_list.html', context)
