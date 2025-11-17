from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models import DailyPuzzle, Play
from app.utils import get_translations
import csv
import random

@login_required
def wordle_view(request):
    language = request.user.userinfo.language
    now = datetime.now()
    context = {'translations': get_translations(language), "language": language, "solved": 0}


    with open('app/static/sanat.csv', newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)
        data = [part[0].replace("Ã", "ä").replace("Ã", "ö") for part in data]

        daily = DailyPuzzle.objects.filter(type="wordle", created_at__date=date(now.year, now.month, now.day))
        if len(daily) > 0:
            word = daily[0].solution
        else:
            word = random.choice(data)
            DailyPuzzle.objects.create(type="wordle", solution=word)
            daily = DailyPuzzle.objects.filter(type="wordle", created_at__date=date(now.year, now.month, now.day))
        context['word'] = word
        context['words'] = data

    #Create Play object if player has finished the wordle
    if request.method == "POST":
        Play.objects.create(puzzle=daily[0], player=request.user, attempts=request.POST['attempts'], time=request.POST['time'])

    plays = Play.objects.filter(puzzle=daily[0], created_at__date=date(now.year, now.month, now.day), player=request.user)
    if len(plays) > 0:
        context['attempted'] = 1
        context['attempts'] = plays[0].attempts


    return render(request, 'wordle.html', context)