from django.shortcuts import render

from dogs.models import Breed, Dog

def index_view(request):
    context = {
        'objects_list': Breed.objects.all()[:3],
        'title': "Питомник - Главное"
    }
    return render(request, 'dogs/index.html', context=context)
