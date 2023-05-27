from django.shortcuts import render


def main_page(request):

    return render(request, 'main_page.html', {})

def login(request):

    return render(request, 'login.html', {})

def signup(request):
    return render(request, 'signup.html', {})