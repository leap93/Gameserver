from django.shortcuts import render
from app.utils import get_translations


def front_page_view(request):

    language = request.GET.get('language')
    context = {'translations': get_translations(language), "language": language}
    return render(request, 'front_page.html', context)