from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from reviews.forms.theme import CustomThemeForm
from reviews.forms.user import CustomUserCreationForm
from reviews.models.models import Theme


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


@login_required
def theme(request):
    user = get_user(request)
    themes = Theme.objects.filter(Q(user_id=None) | Q(user_id=user.id)).order_by('theme_id')
    return render(request, 'theme.html.jinja2', {'themes': themes})


@login_required
def themeadd(request):
    if request.method == 'POST':
        theme_form = CustomThemeForm(request.POST)
        if theme_form.is_valid():
            new_theme = theme_form.save(commit=False)
            new_theme.user_id = request.user
            if theme_form.cleaned_data['is_public']:
                new_theme.user_id = None
            new_theme.save()
            return redirect('theme')

    return render(request, 'theme-add.html.jinja2')


def delete_row(request, row_id):
    row = Theme.objects.get(theme_id=row_id)
    row.delete()
    return redirect('theme')


def company(request):
    return render(request, 'company.html.jinja2', {})


def request(request):
    return render(request, 'analysis.html.jinja2', {})


def learning_reviews(request):
    return render(request, 'learning-reviews.html.jinja2', {})


def learning(request):
    return render(request, 'learning.html.jinja2', {})
