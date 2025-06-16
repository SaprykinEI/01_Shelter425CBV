from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from reviews.models import Review
from users.models import User, UserRoles
from reviews.forms import ReviewAdminForm
from reviews.utils import slug_generator


class ReviewListView(ListView):
    """
        Представление для отображения списка активных отзывов.
        Использует пагинацию (по 3 элемента) и фильтрацию по `sign_of_review=True`.
        """
    model = Review
    extra_context = {
        'title': 'Все отзывы'
    }
    template_name = 'reviews/reviews.html'
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(sign_of_review=True)


class ReviewDeactivatedListView(ListView):
    """
        Представление для отображения списка деактивированных отзывов.
        Фильтрует отзывы с `sign_of_review=False`.
        """
    model = Review
    extra_context = {
        'title': 'Деактивированные отзывы'
    }
    template_name = 'reviews/reviews.html'
    paginate_by = 3

    def get_queryset(self):
        """Фильтрует только деактивированные отзывы."""
        return super().get_queryset().filter(sign_of_review=False)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
        Представление для создания нового отзыва.
        Доступно только авторизованным пользователям с ролью USER или ADMIN.
        При сохранении автоматически устанавливает автора и генерирует slug при необходимости.
        """
    model = Review
    form_class = ReviewAdminForm
    template_name = 'reviews/create_update.html'
    extra_context = {
        'title': 'Добавить отзыв'
    }

    def form_valid(self, form):
        """Проверяет права, устанавливает автора и slug, затем сохраняет отзыв."""
        if self.request.user.role not in [UserRoles.USER, UserRoles.ADMIN]:
            return HttpResponseForbidden
        slug_object = form.save()
        print(slug_object.slug)
        if slug_object.slug == 'temp_slug':
            slug_object.slug = slug_generator()
            print(slug_object.slug)
        slug_object.author = self.request.user
        slug_object.save()
        return super().form_valid(form)


class ReviewDetailView(DetailView):
    """
        Представление для отображения одного отзыва (по slug).
        """
    model = Review
    template_name = 'reviews/detail.html'
    extra_context = {
        'title': "Просмотр отзыва"
    }


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """
        Представление для редактирования отзыва.
        Доступно только автору отзыва, администратору или модератору.
        """
    model = Review
    form_class = ReviewAdminForm
    template_name = 'reviews/create_update.html'
    extra_context = {
        'title': 'Изменить отзыв'
    }

    def get_object(self, queryset=None):
        """Проверяет права доступа к редактированию отзыва."""
        object_ = super().get_object(queryset=queryset)
        if object_.author != self.request.user and self.request.user.role not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            raise PermissionDenied()
        return object_

    def get_success_url(self):
        """Возвращает URL после успешного редактирования."""
        return reverse('review:review_detail', args=[self.kwargs.get('slug')])


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    """
        Представление для удаления отзыва.
        Требует права `reviews.delete_review`.
        """
    model = Review
    template_name = 'reviews/delete.html'
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        """Возвращает URL после успешного удаления."""
        return reverse('reviews:reviews_list')


def review_toggle_activity(request, slug):
    """
        Включает или выключает активность отзыва.
        Если отзыв активен — деактивирует и наоборот.
        После изменения делает редирект на соответствующий список.
        """
    review_item = get_object_or_404(Review, slug=slug)
    if review_item.sign_of_review:
        review_item.sign_of_review = False
        review_item.save()
        return redirect(reverse('reviews:reviews_deactivated_list'))
    else:
        review_item.sign_of_review = True
        review_item.save()
        return redirect(reverse('reviews:reviews_list'))
