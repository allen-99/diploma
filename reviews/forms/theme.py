from django.forms import ModelForm, forms

from reviews.models.models import Theme


class CustomThemeForm(ModelForm):
    class Meta:
        model = Theme
        fields = ['theme_name', 'theme_description', 'is_public']

    def clean_theme_description(self):
        data = self.cleaned_data.get('theme_description')
        if data:
            keywords = [keyword.strip() for keyword in data.split(',')]
            for keyword in keywords:
                if not keyword.strip().isalpha():
                    raise forms.ValidationError('Ключевые слова должны содержать только буквы')
        return data
