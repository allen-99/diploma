import csv
from datetime import datetime

import pytz
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from reviews.forms.company import CustomCompanyForm
from reviews.forms.theme import CustomThemeForm
from reviews.forms.user import CustomUserCreationForm
from reviews.learning.learn import Learn
from reviews.models.models import Theme, Company, SetOfText, Text, Model


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
    user = get_user(request)
    return render(request, 'lk.html.jinja2', {'user': user})


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


def delete_theme(request, row_id):
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
def delete_company(request, row_id):
    row = Company.objects.get(company_id=row_id)
    row.delete()
    return redirect('company')


@login_required
def delete_reviews(request, row_id):
    row = SetOfText.objects.get(set_id=row_id)
    row.delete()
    return redirect('learnreviews')


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
                date = row[1]

                reviews.append([text, date])
        except:
            return render(request, 'reviews-add.html.jinja2', {'companies': companies})
        if len(reviews):
            company = companies.get(company_id=request.POST.get('company_id'))
            set_of_text = SetOfText()
            set_of_text.name = request.POST.get('name')
            set_of_text.is_public = request.POST.get('is_public') == 'on'
            set_of_text.user = user
            set_of_text.company = company
            set_of_text.is_learning = False
            set_of_text.save()
            for review in reviews:
                new_review = Text()
                new_review.text = review[0]
                try:
                    new_review.date = datetime.strptime(review[1], '%Y-%m-%dT%H:%M:%S.%fZ')
                except:
                    new_review.date = datetime.strptime(review[1], '%Y-%m-%dT%H:%M:%S%fZ')
                new_review.company = company
                new_review.set = set_of_text
                new_review.save()
        return redirect('company')

    return render(request, 'reviews-add.html.jinja2', {'companies': companies})


@login_required
def learnreviews(request):
    user = get_user(request)
    set_of_texts = SetOfText.objects.filter((Q(user_id=None) | Q(user_id=user.id)) & Q(is_learning=True))
    return render(request, 'learn-reviews.html.jinja2', {'set_of_texts': set_of_texts})


@login_required
def request(request):
    user = get_user(request)
    themes = Theme.objects.filter(Q(user_id=None) | Q(user_id=user.id)).order_by('theme_id')
    companies = Company.objects.filter(Q(user_id=None) | Q(user_id=user.id)).order_by('company_id')
    models = Model.objects.filter(Q(user_id=None) | Q(user_id=user.id)).order_by('id')

    return render(request, 'analysis.html.jinja2', {'themes': themes, 'companies': companies, 'models': models})


@login_required
def learning_reviews(request):
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
                rating = row[1]
                date = row[2]

                reviews.append([text, rating, date])
        except:
            return render(request, 'learning-reviews.html.jinja2', {'companies': companies})

        if len(reviews):
            company = companies.get(company_id=request.POST.get('company_id'))
            set_of_text = SetOfText()
            set_of_text.name = request.POST.get('name')
            set_of_text.is_public = request.POST.get('is_public') == 'on'
            set_of_text.user = user
            set_of_text.company = company
            set_of_text.is_learning = True
            set_of_text.save()
            for review in reviews:
                new_review = Text()
                new_review.text = review[0]
                new_review.rating = int(review[1])
                try:
                    new_review.date = datetime.strptime(review[2], '%Y-%m-%dT%H:%M:%S.%fZ')
                except:
                    new_review.date = datetime.strptime(review[2], '%Y-%m-%dT%H:%M:%S%fZ')
                new_review.date = new_review.date.replace(tzinfo=pytz.UTC)
                new_review.company = company
                new_review.set = set_of_text
                new_review.save()
            return redirect('learnreviews')
    return render(request, 'learning-reviews.html.jinja2', {'companies': companies})


@login_required
def learning(request):
    user = get_user(request)
    set_of_texts = SetOfText.objects.filter((Q(user_id=None) | Q(user_id=user.id)) & Q(is_learning=True))
    if request.method == 'POST':
        name = request.POST.get('name')
        algorithm = request.POST.get('algorithm')
        set_of_text = request.POST.get('set_of_text')
        Learn.learn(name, algorithm, set_of_text)
        return redirect('lk')

    return render(request, 'learning.html.jinja2', {'set_of_texts': set_of_texts})
