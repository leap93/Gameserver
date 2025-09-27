from django.shortcuts import render

from app.utils import get_translations


def sudoku_view(request):
    language = request.user.userinfo.language
    context = {'translations': get_translations(language), "language": language}

    return render(request, 'sudoku.html', context)