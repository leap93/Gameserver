import json
from datetime import datetime, date, time
from Gameserver.views.sudoku_view import random_sudoku, solve_recursive_up
from app.models import DailyPuzzle

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Creates a daily sudoku puzzle'

    def handle(self, *args, **options):
        now = datetime.now()
        daily = DailyPuzzle.objects.filter(type="sudoku", created_at__date=date(now.year, now.month, now.day))
        if len(daily) == 0:
            sudoku = random_sudoku()
            DailyPuzzle.objects.create(type="sudoku", puzzle_text=json.dumps(sudoku), solution=json.dumps(solve_recursive_up(sudoku, -1, 0, time.time() + 10)))
            self.stdout.write(self.style.SUCCESS('Sudoku created!'))
        else:
            self.stdout.write(self.style.SUCCESS('Sudoku already exists!'))


