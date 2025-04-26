from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


from dogs.models import Breed, Dog
from dogs.forms import DogForm


def index_view(request):
    """Функция отвечает за отображение главной страницы питомника."""
    context = {
        'objects_list': Breed.objects.all()[:3],
        'title': "Питомник - Главная"
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


class DogListView(ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - все наши собаки'
    }
    template_name = 'dogs/dogs.html'


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    extra_context = {
        'title': 'Добавить собаку'
    }
    success_url = reverse_lazy('dogs:dogs_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data['title'] = f'Подробная информация {object_}'
        return context_data


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data['title'] = f'Изменить собаку {object_}'
        return context_data

    def get_success_url(self):
        return reverse('dogs:dog_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:dogs_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_ = self.get_object()
        context_data['title'] = f'Удалить собаку {object_}'
        return context_data