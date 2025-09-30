import json
from datetime import datetime, date, time
from Gameserver.views.sudoku_view import random_sudoku
from app.models import DailyPuzzle

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        now = datetime.now()
        daily = DailyPuzzle.objects.filter(type="sudoku", created_at__date=date(now.year, now.month, now.day))
        if len(daily) == 0:
            DailyPuzzle.objects.create(type="sudoku", puzzle_text=json.dumps(random_sudoku()))
            self.stdout.write(self.style.SUCCESS('Sudoku created!'))
        else:
            raise CommandError('Daily sudoku already exists')



