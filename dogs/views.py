from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from dogs.models import Breed, Dog
from dogs.forms import DogForm

def index_view(request):
    """Функция отвечает за отображение главной страницы питомника."""
    context = {
        'objects_list': Breed.objects.all()[:3],
        'title': "Питомник - Главное"
    }
    return render(request, 'dogs/index.html', context=context)

def breeds_list_view(request):
    """Функция отображает список всех пород собак, доступных в питомнике."""
    context = {
        'objects_list': Breed.objects.all(),
        'title': "Питомник - Все наши породы"
    }
    return render(request, 'dogs/breeds.html',context=context)

def breed_dogs_list_view(request, pk: int):
    """Отображение списка собак определенной породы."""
    breed_object = Breed.objects.get(pk=pk)
    context = {
        'objects_list': Dog.objects.filter(breed_id=pk),
        'title': f"Собаки породы - {breed_object.name}",
        'breed_pk': breed_object.pk
    }
    return render(request, 'dogs/dogs.html', context=context)

#Create Read Update Delete(CRUD)

def dogs_list_view(request):
    """Вывод списка всех собак на отдельной странице"""
    context = {
        'objects_list': Dog.objects.all(),
        'title': f"Все наши собаки",
    }
    return render(request, 'dogs/dogs.html', context=context)

def dog_create_view(request):
    """ Создание новой собаки в базе данных через форму"""
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dogs:dogs_list'))
    context = {
        'title': 'Добавить собаку',
        'form': DogForm
    }
    return render(request, 'dogs/create.html', context=context)

def dog_detail_view(request, pk):
    """Обрабатывает запрос для отображения подробной информации"""
    dog_object = Dog.objects.get(pk=pk)
    context = {
        'object': dog_object,
        'title': dog_object,
    }
    return render(request, 'dogs/detail.html', context=context)

