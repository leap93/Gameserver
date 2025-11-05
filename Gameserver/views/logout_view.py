from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from app.utils import get_translations

@login_required
def logout_view(request):
    language = request.user.userinfo.language
    logout(request)
    translations = get_translations(language)
    context = {'translations': translations, 'language': language}
    return render(request, 'logout.html', context)
