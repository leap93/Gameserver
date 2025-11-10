from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.utils import get_translations


@login_required
def chess_view(request):
    language = request.user.userinfo.language
    context = {'translations': get_translations(language), "language": language}
    return render(request, 'chess.html', context)