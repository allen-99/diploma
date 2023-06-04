from django.conf import settings
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('login', LoginView.as_view(next_page=settings.LOGIN_REDIRECT_URL, template_name='login.html.jinja2'),
         name='login'),
    path('signup', views.signup, name='signup'),
    path('lk', views.lk, name='lk'),
    path('theme', views.theme, name='theme'),
    path('themeadd', views.themeadd, name='themeadd'),
    path('delete/<int:row_id>/', views.delete_row, name='delete_row'),
    path('company', views.company, name='company'),
    path('request', views.request, name='request'),
    path('reviews', views.learning_reviews, name='reviews'),
    path('learning', views.learning, name='learning'),
    path('logout', LogoutView.as_view(next_page='', template_name='main_page.html.jinja2'), name='logout'),
]
