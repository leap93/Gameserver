"""
URL configuration for Gameserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from Gameserver.views import login_view, register_view, front_page_view, sudoku_view, logout_view, wordle_view

urlpatterns = [
    path('login/', login_view.login_view, name='login'),
    path('register/', register_view.register_view, name='register'),
    path('front_page/', front_page_view.front_page_view, name='front_page'),
    path('sudoku/', sudoku_view.sudoku_view, name='sudoku'),
    path('wordle/', wordle_view.wordle_view, name='wordle'),
    path('logout/', logout_view.logout_view, name='logout'),

]
