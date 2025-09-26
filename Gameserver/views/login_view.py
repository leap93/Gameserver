from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from app.utils import get_translations


def login_view(request):
    return login_function(request, request.GET.get('language'))

def login_view_after_register(request, language):
    return login_function(request, language)

def login_function(request, language):
    #Translations
    context = {'translations': get_translations(language), "language": language}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        #succsesfull login
        if user is not None:
            login(request, user)
            return redirect('front_page')
        #invalid user or password
        else:
            return invalid_username_or_password(request, username, context)
    #redirection from a page that requires a login
    if 'next' in request.GET:
        context['message'] = context["translations"]["this page requires a login"]
        return render(request, 'login.html', context)
    return render(request, 'login.html', context)

def invalid_username_or_password(request, username, context):
    context['message'] = context["translations"]["invalid username or password"]
    context['username'] = username
    return render(request, 'login.html', context)