from django.shortcuts import render


def main_page(request):
    return render(request, 'main_page.html.jinja2', {})

def login(request):
    return render(request, 'login.html.jinja2', {})

def signup(request):
    return render(request, 'signup.html.jinja2', {})

def main_signin_page(request):
    return render(request, 'signup.html.jinja2', {})

def lk(request):
    return render(request, 'lk.html.jinja2', {})

def theme(request):
    return render(request, 'theme.html.jinja2', {})

def company(request):
    return render(request, 'company.html.jinja2', {})

def request(request):
    return render(request, 'analysis.html.jinja2', {})

def learning_reviews(request):
    return render(request, 'learning-reviews.html.jinja2', {})

def learning(request):
    return render(request, 'learning.html.jinja2', {})