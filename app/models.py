from django.db import models
from django.contrib.auth.models import User

LANGUAGES = (
    ('en', 'English'),
    ('fi', 'Finnish'),
)

TYPE = (
    ('sudoku', 'Sudoku'),
)

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=100, choices=LANGUAGES)
    class Meta:
        app_label = 'Gameserver'

class DailyPuzzle(models.Model):
    type = models.CharField(max_length=100, choices=TYPE)
    puzzle_text = models.TextField(max_length=511)
    solution = models.TextField(max_length=511)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'Gameserver'

class Play(models.Model):
    puzzle = models.ForeignKey(DailyPuzzle, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.IntegerField()
    attempts = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'Gameserver'