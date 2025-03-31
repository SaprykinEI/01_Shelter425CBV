from django import forms

from dogs.models import Dog

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'