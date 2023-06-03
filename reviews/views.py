from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from reviews.forms.user import CustomUserCreationForm


def main_page(request):
    return render(request, 'main_page.html.jinja2', {})


def signup(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('lk')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'signup.html.jinja2', {'user_form': user_form})


# def logout(request):


def main_signin_page(request):
    return render(request, 'signup.html.jinja2', {})


@login_required
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
