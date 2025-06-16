from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
        Класс админки для модели User.

        Атрибуты:
            list_display: кортеж полей для отображения в списке пользователей (pk, email, фамилия, имя, роль, активность).
            list_filter: кортеж полей для фильтрации списка (фамилия).
        """
    list_display = ('pk', 'email', 'last_name', 'first_name', 'role', 'is_active',)
    list_filter = ('last_name',)
