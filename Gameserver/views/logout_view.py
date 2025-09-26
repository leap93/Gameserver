from django.shortcuts import render
from django.contrib.auth import logout
from app.utils import get_translations

def logout_view(request):
    language = request.GET.get('language')
    logout(request)
    translations = get_translations(language)
    context = {'translations': translations, 'language': language}
    return render(request, 'logout.html', context)
