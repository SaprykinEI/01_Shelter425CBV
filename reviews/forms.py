from django import forms
from reviews.models import Review
from users.forms import StyleFormMixin


class ReviewAdminForm(StyleFormMixin, forms.ModelForm):
    """Форма администратора для создания и редактирования отзывов."""
    title = forms.CharField(max_length=150, label='Заголовок')
    content = forms.TextInput()
    slug = forms.SlugField(max_length=20, initial='temp_slug', widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ('dog', 'title', 'content', 'slug')
