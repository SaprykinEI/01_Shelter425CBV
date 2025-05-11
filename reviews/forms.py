from django import forms
from reviews.models import Review
from users.forms import StyleFormMixin

class ReviewAdminForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ('dog', 'title', 'content', 'slug')