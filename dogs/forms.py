import datetime

from django import forms

from dogs.models import Dog, DogParent
from users.forms import StyleFormMixin


class DogForm(StyleFormMixin, forms.ModelForm):
    """
        Форма для создания и редактирования объекта Dog пользователями.

        Исключает поля:
            - owner: устанавливается автоматически при создании.
            - is_active: доступно только админам.
            - views: изменяется автоматически при просмотре.

        Методы:
            clean_birth_date(): Проверяет, что возраст собаки не превышает 35 лет.
        """
    class Meta:
        model = Dog
        exclude = ('owner', 'is_active', 'views',)

    def clean_birth_date(self):
        clean_data = self.cleaned_data['birth_date']
        now_year = datetime.datetime.now().year
        if now_year - clean_data.year > 35:
            raise forms.ValidationError('Собака должна быть моложе 35 лет')
        return clean_data


class DogAdminForm(DogForm):
    """
        Админ-версия формы Dog, позволяющая редактировать владельца и просмотры.

        Исключает только:
            - is_active: может быть отфильтровано иначе в админке.
        """
    class Meta:
        model = Dog
        exclude = ('is_active',)


class DogParentForm(StyleFormMixin, forms.ModelForm):
    """
        Форма для создания и редактирования информации о родителях собаки.

        Использует все поля модели DogParent.
        """
    class Meta:
        model = DogParent
        fields = '__all__'
