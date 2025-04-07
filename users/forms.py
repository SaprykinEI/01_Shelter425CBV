from django import forms

from users.models import User
from users.validators import validate_password
from django.contrib.auth.forms import PasswordChangeForm


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')


class UserRegisterForm(StyleFormMixin, forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        validate_password(cleaned_data['password'])
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError("Пароли не совпадают!!!")
        return cleaned_data['password2']


class UserLoginForm(StyleFormMixin, forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar')


class UserChangePasswordForm(StyleFormMixin, PasswordChangeForm):
    pass
