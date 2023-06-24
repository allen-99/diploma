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
    path('delete/theme/<int:row_id>/', views.delete_theme, name='delete_theme'),
    path('delete/company/<int:row_id>/', views.delete_company, name='delete_company'),
    path('delete/reviews/<int:row_id>/', views.delete_reviews, name='delete_reviews'),
    path('delete/company/reviews/<int:row_id>/', views.delete_reviews_company, name='delete_reviews_company'),

    path('analysis/<int:id>/', views.analysis, name='analysis'),
    path('company', views.company, name='company'),
    path('company/info/<int:id>', views.company_info, name='companyinfo'),
    path('company/add', views.companyadd, name='companyadd'),
    path('request', views.request, name='request'),
    path('reviews', views.learning_reviews, name='reviews'),
    path('reviews/add', views.reviewsadd, name='reviewsadd'),
    path('learn/reviews', views.learnreviews, name='learnreviews'),
    path('learning', views.learning, name='learning'),
    path('logout', LogoutView.as_view(next_page='', template_name='main_page.html.jinja2'), name='logout'),
    path('result/<int:company>/<int:model>/', views.result, name='result')
]
