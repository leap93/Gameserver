from django.db import models
from django.contrib.auth.models import User

LANGUAGES = (
    ('en', 'English'),
    ('fi', 'Finnish'),
)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=100, choices=LANGUAGES)
    class Meta:
        app_label = 'Gameserver'