from django.db import models

# Create your models here.

class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name='breed')
    description = models.CharField(max_length=1000, verbose_name='description')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'