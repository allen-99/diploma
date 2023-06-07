from django.forms import ModelForm

from reviews.models.models import Company


class CustomCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'is_public']
