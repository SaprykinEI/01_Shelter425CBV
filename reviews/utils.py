import string
import random


def slug_generator():
    """
     Генерирует случайный slug длиной 20 символов, состоящий из букв латинского алфавита и цифр.

     Returns:
         str: Уникальная строка, подходящая для использования в качестве slug.
     """
    return ''.join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=20))
