from django.urls import path
from dogs.apps import DogsConfig

from dogs.views import index_view, breeds_list_view, breed_dogs_list_view

app_name = DogsConfig.name

urlpatterns = [
    path('', index_view, name='index'),
    path('breeds/', breeds_list_view, name='breeds'),
    path('breeds/<int:pk>/dogs/', breed_dogs_list_view, name='breed_dogs'),

]