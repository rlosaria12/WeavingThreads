from django.shortcuts import render
from core.models import Program, SubProgram
from .models import Indicator

def program_indicator(request):
    year = request.GET.get('year')
    selected_program = request.GET.get('program')
    saved = False

    programs = Program.objects.all().order_by('program_number')
    subprograms = None

    if request.method == 'POST':
        year = request.POST.get('year')
        program_id = request.POST.get('program')
        output_indicators = request.POST.getlist('output_indicator')
        target_indicators = request.POST.getlist('target_indicator')
        sub_ids = request.POST.getlist('subprogram_id')

        # Save logic (basic placeholder)
        for sub_id, out_ind, tgt_ind in zip(sub_ids, output_indicators, target_indicators):
            # You could create IndicatorDetail here if needed
            pass

        saved = True

    if selected_program:
        subprograms = SubProgram.objects.filter(program_id=selected_program).order_by('subprogram_number')

    context = {
        'year': year,
        'programs': programs,
        'selected_program': selected_program,
        'subprograms': subprograms,
        'saved': saved,
    }

    return render(request, 'admin/indicator/program_indicator.html', context)
