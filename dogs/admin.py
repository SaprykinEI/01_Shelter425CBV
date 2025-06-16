from django.contrib import admin
from dogs.models import Breed, Dog
# Register your models here.


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    """
        Админ-интерфейс для модели Breed.

        Отображает:
            - pk: первичный ключ.
            - name: название породы.

        Сортировка по:
            - pk (по возрастанию).
        """
    list_display = ('pk', 'name')
    ordering = ('pk',)


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    """
        Админ-интерфейс для модели Dog.

        Отображает:
            - pk: первичный ключ.
            - name: кличка собаки.
            - breed: порода.
            - owner: владелец.

        Фильтрация по:
            - breed (порода).

        Сортировка по:
            - name (по алфавиту).
        """
    list_display = ('pk', 'name', 'breed', 'owner', )
    list_filter = ('breed',)
    ordering = ('name',)
