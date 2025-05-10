from django.conf import settings
from django.core.cache import cache

from  dogs.models import Breed


def get_breed_cache():
    if settings.CACHE_ENABLED:
        key = 'breed_list'
        breed_list = cache.get(key)
        if breed_list is None:
            breed_list = Breed.objects.all()
            cache.set(key, breed_list)
    else:
        breed_list = Breed.objects.all()

    return breed_list