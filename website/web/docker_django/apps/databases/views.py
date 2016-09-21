from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from .models import MUTANTS

@login_required
def mutant_database(request):
    all_mutants = MUTANTS.objects.all().order_by('-ADDED_TO_DB')
    return render(request, 'databases/mutant-database.html', {'all_mutants': all_mutants,})

from watson import search as watson
@login_required
def MUTANT_search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            search_results = watson.filter(MUTANTS, q)
            return render(request, 'databases/search-results.html', {'search_results': search_results, 'query': q})
    return redirect('mutant-database')
