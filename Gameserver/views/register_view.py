from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from app.utils import get_translations


def register_view(request):
    #translations

    if request.method == "POST":
        language = request.POST['language']
    else:
        language = request.GET.get('language')

    if language == "" or language is None:
        language = 'en'

    context = {'translations': get_translations(language), 'language': language}

    if request.method == 'POST':
        #create user
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        try:
            user = User.objects.create_user(username, email, password)
            context["message"] = context["translations"]["register_success"]
        except IntegrityError:
            context["message"] = context["translations"]["username_exists"]
            context["username"] = username
            context["email"] = email
    return render(request, 'register.html', context)