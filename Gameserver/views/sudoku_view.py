from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from app.utils import get_translations


def sudoku_view(request):
    language = request.GET.get('language')
    context = {'translations': get_translations(language), "language": language}

    return render(request, 'sudoku.html', context)