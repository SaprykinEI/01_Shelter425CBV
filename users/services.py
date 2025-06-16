from django.conf import settings
from django.core.mail import send_mail


def send_register_email(email):
    """
        Отправляет письмо с поздравлением о регистрации на сервисе.

        Аргументы:
            email (str): Адрес электронной почты получателя.
        """
    send_mail(
        subject="Поздравляем с регистрацией на нашем сервисе",
        message="Вы успешно зарегистрировались на сервисе Shelter425",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email, ]
    )


def send_new_password(email, new_password):
    """
        Отправляет письмо с новым паролем пользователю.

        Аргументы:
            email (str): Адрес электронной почты получателя.
            new_password (str): Новый пароль для пользователя.
        """
    send_mail(
        subject="Вы успешно изменили пароль",
        message=f"Ваш новый пароль: {new_password}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email, ]
    )
