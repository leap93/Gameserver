from datetime import datetime, date

from django.shortcuts import render

from app.models import DailyPuzzle
from app.utils import get_translations
import csv
import random

def wordle_view(request):
    language = request.user.userinfo.language
    now = datetime.now()
    daily = DailyPuzzle.objects.filter(type="wordle", created_at__date=date(now.year, now.month, now.day))
    context = {'translations': get_translations(language), "language": language, "solved": 0}

    with open('app/static/sanat.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        word = random.choice(data)[0]
        context['word'] = word
        context['words'] = data

    return render(request, 'wordle.html', context)