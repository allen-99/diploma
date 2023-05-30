from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('lk', views.lk, name='lk'),
    path('theme', views.theme, name='theme'),
    path('company', views.company, name='company'),
    path('request', views.request, name='request'),
    path('reviews', views.learning_reviews, name='reviews'),
    path('learning', views.learning, name='learning'),
]