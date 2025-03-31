from django.urls import path
from dogs.apps import DogsConfig

from dogs.views import (index_view, breeds_list_view, breed_dogs_list_view, dog_create_view, dogs_list_view,
                        dog_detail_view, dog_update_view, dog_delete_view)

app_name = DogsConfig.name

urlpatterns = [
    # breeds
    path('', index_view, name='index'),
    path('breeds/', breeds_list_view, name='breeds'),

    #dogs
    path('breeds/<int:pk>/dogs/', breed_dogs_list_view, name='breed_dogs'),
    path('dogs/', dogs_list_view, name='dogs_list'),
    path('dogs/create', dog_create_view, name='dog_create'),
    path('dogs/detail/<int:pk>/', dog_detail_view, name='dog_detail'),
    path('dogs/update/<int:pk>', dog_update_view, name='dog_update'),
    path('dogs/delete/<int:pk>', dog_delete_view, name='dog_delete')

]