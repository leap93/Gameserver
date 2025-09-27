from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app.models import LANGUAGES
from app.utils import get_translations

@login_required
def front_page_view(request):
    language = request.user.userinfo.language
    context = {'translations': get_translations(language), "language": language, 'languages': LANGUAGES}
    return render(request, 'front_page.html', context)