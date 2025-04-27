import datetime

from django import forms

from dogs.models import Dog, DogParent
from users.forms import StyleFormMixin

class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ('owner',)

    def clean_birth_date(self):
        clean_data = self.cleaned_data['birth_date']
        now_year = datetime.datetime.now().year
        if now_year - clean_data.year > 35:
            raise forms.ValidationError('Собака должна быть моложе 35 лет')
        return clean_data


class DogParentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = DogParent
        fields = '__all__'