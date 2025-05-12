from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from reviews.models import Review
from users.models import User
from reviews.forms import ReviewAdminForm


class ReviewListView(ListView):
    model = Review
    extra_context = {
        'title': 'Все отзывы'
    }
    template_name = 'reviews/reviews.html'

    def get_queryset(self):
        return super().get_queryset().filter(sign_of_review=True)


class ReviewDeactivatedListView(ListView):
    model = Review
    extra_context = {
        'title': 'Деактивированные отзывы'
    }
    template_name = 'reviews/reviews.html'

    def get_queryset(self):
        return super().get_queryset().filter(sign_of_review=False)

