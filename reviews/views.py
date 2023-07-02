import csv
import json
from datetime import datetime

import maya
import numpy as np
import pytz
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse

from reviews.analysis.analysis import Analysis
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


@login_required
def delete_theme(request, row_id):
    row = Theme.objects.get(theme_id=row_id)
    row.delete()
    return redirect('theme')


@login_required
def company(request):
    user = get_user(request)
    companies = Company.objects.filter((Q(is_public=True) | Q(user_id=user.id))).order_by('company_id')
    for company in companies:
        reviews = SetOfText.objects.filter(Q(company_id=company) & Q(is_learning=False))
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


def company_info(request, id):
    user = get_user(request)
    company = Company.objects.get(company_id=id)
    sets = SetOfText.objects.filter((Q(user_id=None) | Q(user_id=user.id)) & Q(is_learning=False) & Q(company_id=id))
    return render(request, 'company-info.html.jinja2', {'company': company, 'sets': sets})


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
def delete_reviews_company(request, row_id):
    row = SetOfText.objects.get(set_id=row_id)
    row.delete()
    return redirect('company')


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
                reviews.append({'text': row[0], 'date': row[1]})
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
                new_review.text = review['text']
                print(review['date'])
                try:
                    dt = maya.parse(review['date']).datetime()
                    new_review.date = dt.date()
                except:
                    try:
                        new_review.date = datetime.strptime(review['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    except:
                        new_review.date = datetime.strptime(review['date'], '%Y-%m-%dT%H:%M:%S%fZ')

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
    companies = Company.objects.filter(
        (Q(is_public=True) | Q(user_id=user.id)) & Q(setoftext__isnull=False) & Q(
            setoftext__is_learning=False)).distinct().order_by('company_id')
    if request.method == 'POST':
        id = request.POST.get('company')
        if id is None:
            return redirect('request')
        return redirect('analysis', id=id)
    return render(request, 'analysis.html.jinja2', {'companies': companies})


@login_required
def analysis(request, id):
    user = get_user(request)
    themes = Theme.objects.filter(Q(user_id=None) | Q(user_id=user.id)).order_by('theme_id')
    company = Company.objects.get(company_id=id)
    set_of_texts = SetOfText.objects.filter(
        (Q(user_id=None) | Q(user_id=user.id)) & Q(is_learning=False) & Q(company_id=id))
    models = Model.objects.filter(Q(user_id=None) | Q(user_id=user.id)).order_by('id')

    if request.method == 'POST':
        model = request.POST.get('model')
        chosen_sets_ids = request.POST.getlist('sets')
        chosen_themes_ids = request.POST.getlist('themes')
        url = reverse('result', kwargs={'model': model, 'company': id})
        url += '?csi=' + ','.join(chosen_sets_ids)
        url += '&cti=' + ','.join(chosen_themes_ids)

        if len(''.join(chosen_sets_ids)) == 0:
            return render(request, 'analysis2.html.jinja2', {
                'themes': themes,
                'models': models,
                'set_of_texts': set_of_texts,
                'company': company,
            })
        return redirect(url)

    return render(request, 'analysis2.html.jinja2', {
        'themes': themes,
        'models': models,
        'set_of_texts': set_of_texts,
        'company': company,
    })


@login_required
def result(request, company, model):
    model_id = model
    company_id = company
    chosen_sets_ids = request.GET.get('csi')
    chosen_themes_ids = request.GET.get('cti')
    additional_analysis = request.GET.get('aa')
    company_info = Company.objects.get(company_id=company_id)

    themes = []
    if len(chosen_themes_ids) != 0:
        themes = [int(i) for i in chosen_themes_ids.split(',')]
        themes = Theme.objects.filter(theme_id__in=themes)
        themes = list(themes.values_list('theme_name', flat=True))

    analysis_block = Analysis(company_id, model_id, chosen_sets_ids, chosen_themes_ids, additional_analysis)
    analysis_result = analysis_block.analysis()
    sa_counts = []
    date_dynamic = []
    sa_means = []
    all_sa_mean_float = []
    date_r = []

    for df in analysis_result:
        sa_config = df.groupby('sa', as_index=False).count()
        sa_mean_float = df['sa'].mean()
        all_sa_mean_float.append(sa_mean_float)
        sa_mean = "{:.2f}".format(sa_mean_float)
        sa_means.append(sa_mean)
        date = df['date'].dt.date.tolist()
        date = json.dumps(date, indent=4, sort_keys=True, default=str)
        date_result = [date, df['sa'].values.tolist()]
        sa_config['sa'] = sa_config['sa'].replace(1, "Ужасно")
        sa_config['sa'] = sa_config['sa'].replace(2, "Плохо")
        sa_config['sa'] = sa_config['sa'].replace(3, "Удовлетворительно")
        sa_config['sa'] = sa_config['sa'].replace(4, "Хорошо")
        sa_config['sa'] = sa_config['sa'].replace(5, "Прекрасно")

        sa_config = sa_config.T.values.tolist()
        sd = []
        for sa in sa_config:
            sd.append(sa)
        sa_counts.append(sd[:2])
        date_dynamic.append(date_result)
        date_r += date_result
    all_sa = json.dumps(sa_counts.pop(), ensure_ascii=False)
    all_date = json.dumps(date_dynamic.pop(), ensure_ascii=False)
    sa_counts = json.dumps(sa_counts, ensure_ascii=False)
    date_dynamic = json.dumps(date_dynamic, ensure_ascii=False)
    themes_sa = zip(themes, sa_means)
    all_sa_mean_float = np.array(all_sa_mean_float)
    all_sa_mean_float_mean = "{:.2f}".format(all_sa_mean_float.mean())

    return render(request, 'result.html.jinja2', {
        'sa_counts': sa_counts,
        'themes_sa': themes_sa,
        'company': company_info,
        'date_dynamic': date_dynamic,
        'mean': all_sa_mean_float_mean,
        'all_sa': all_sa,
        'all_date': all_date,
    })


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
        my_learn = Learn()
        my_learn.learn(name, algorithm, set_of_text)
        return redirect('lk')

    return render(request, 'learning.html.jinja2', {'set_of_texts': set_of_texts})
