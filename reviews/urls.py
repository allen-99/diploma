from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup')
]