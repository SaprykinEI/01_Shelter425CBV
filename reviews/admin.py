from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админская конфигурация для модели Review."""
    list_display = ('title', 'dog', 'author',)
