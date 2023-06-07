import csv
from datetime import datetime

from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from reviews.forms.company import CustomCompanyForm
from reviews.forms.theme import CustomThemeForm
from reviews.forms.user import CustomUserCreationForm
from reviews.models.models import Theme, Company, SetOfText, Text


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
            new_theme.user = request.user
            if theme_form.cleaned_data['is_public']:
                new_theme.user = None
            new_theme.save()
            return redirect('theme')

    return render(request, 'theme-add.html.jinja2')


def delete_row(request, row_id):
    row = Theme.objects.get(theme_id=row_id)
    row.delete()
    return redirect('theme')


@login_required
def company(request):
    user = get_user(request)
    companies = Company.objects.filter(Q(user_id=None) | Q(user_id=user.id)).order_by('company_id')
    for company in companies:
        reviews = SetOfText.objects.filter(company_id=company)
        company.has_reviews = len(reviews)
    return render(request, 'company.html.jinja2', {'companies': companies})


@login_required
def companyadd(request):
    if request.method == 'POST':
        company_form = CustomCompanyForm(request.POST)
        if company_form.is_valid():
            new_company = company_form.save(commit=False)
            new_company.user = request.user
            if company_form.cleaned_data['is_public']:
                new_company.user = None
            new_company.save()
            return redirect('company')
    return render(request, 'company-add.html.jinja2', {})


@login_required
def reviewsadd(request):
    user = get_user(request)
    companies = Company.objects.filter(Q(user_id=None) | Q(user_id=user.id)).order_by('company_id')
    if request.method == 'POST':
        reviews = []
        try:
            csv_file = request.FILES.get('reviews')
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter=',')
            for row in reader:
                text = row[0]
                rating = int(row[1])
                date = row[2]

                reviews.append([text, rating, date])
        except:
            return render(request, 'reviews-add.html.jinja2', {'companies': companies})
        if len(reviews):
            company = companies.get(company_id=request.POST.get('company_id'))
            set_of_text = SetOfText()
            set_of_text.name = request.POST.get('name')
            set_of_text.user = user
            set_of_text.company = company
            set_of_text.save()
            for review in reviews:
                new_review = Text()
                new_review.text = review[0]
                new_review.rating = int(review[1])
                try:
                    new_review.date = datetime.strptime(review[2], '%Y-%m-%dT%H:%M:%S.%fZ')
                except:
                    new_review.date = datetime.strptime(review[2], '%Y-%m-%dT%H:%M:%S%fZ')
                new_review.company = company
                new_review.set = set_of_text
                new_review.save()
        return redirect('company')

    return render(request, 'reviews-add.html.jinja2', {'companies': companies})


def request(request):
    return render(request, 'analysis.html.jinja2', {})


def learning_reviews(request):
    return render(request, 'learning-reviews.html.jinja2', {})


def learning(request):
    return render(request, 'learning.html.jinja2', {})
