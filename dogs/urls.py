from django.urls import path
from dogs.apps import DogsConfig

from dogs.views import index_view

app_name = DogsConfig.name

urlpatterns = [
    path('', index_view, name='index')
]