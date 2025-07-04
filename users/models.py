from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    """
        Класс перечисления ролей пользователя.

        Атрибуты:
            ADMIN (str): Роль администратора.
            MODERATOR (str): Роль модератора.
            USER (str): Роль обычного пользователя.
        """
    ADMIN = 'admin', _('admin')
    MODERATOR = 'moderator', _('moderator')
    USER = 'user', _('user')


class User(AbstractUser):
    """Модель пользователя с дополнительными полями и ролью."""
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)
    first_name = models.CharField(max_length=150, verbose_name='Имя', default='Anonymous')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', default='Anonymous')
    phone = models.CharField(max_length=35, unique=True, verbose_name='Телефон', **NULLABLE)
    telegram = models.CharField(max_length=150, unique=True, verbose_name='Телеграм', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Автар', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """Возвращает строковое представление пользователя — его email."""
        return f'{self.email}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']
