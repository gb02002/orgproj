from typing import Protocol

import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, UpdateView, FormView, CreateView

from orgs.forms import LocationMediaForm, LocationsForm, OrgForm
from orgs.models import LocationMedia, Locations, Organisation

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Class1(Protocol):
    pass


"""
AddOrg
AddLocforExistingOrgView
DelOrgView
DelLocOfOrgView
EditOrgView
EditLocView
AddLocMedia
EditLocMediaView
DelLocMediaView
"""


class AddOrg(LoginRequiredMixin, CreateView):
    template_name = 'add_org_1.html'
    success_url = reverse_lazy("edit-choice")  # Подставьте ваш URL
    org_form_class = OrgForm
    model = Organisation
    fields = ['title', 'desc', 'mail', 'phone', 'web']

    def form_valid(self, form):
        form.instance.agent = self.request.user  # Set the agent field to the current user
        logger.info(f'Adding new org for {self.request.user}')
        return super().form_valid(form)


class AddLocforExistingOrgView(LoginRequiredMixin, CreateView):
    template_name = 'add_loc.html'
    org_form_class = LocationsForm
    model = Locations
    fields = ['location_name', 'address', 'open_hours', 'point', 'filter']

    def form_valid(self, form):
        org_id = self.kwargs['pk']
        org = Organisation.objects.get(pk=org_id)  # Получаем объект Org по org_id
        form.instance.related_org = org
        logger.info(f'Adding loc for {org_id}')
        return super().form_valid(form)

    def get_success_url(self):
        logger.info(f'Redirection of success')
        return reverse('edit-choice')  # Подставьте ваш URL


class DelOrgView(LoginRequiredMixin, DeleteView):
    model = Organisation
    template_name = 'confirm_delete_org.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('edit-choice')  # URL для перенаправления после успешного удаления

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Organisation.objects.get(pk=pk)

    def delete(self, request, *args, **kwargs):
        logger.info(f'Deleted org {self.kwargs.get('pk')}')
        return super().delete(request, *args, **kwargs)


class DelLocOfOrgView(LoginRequiredMixin, DeleteView):
    model = Locations
    template_name = 'confirm_delete_loc.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('edit-choice')  # URL для перенаправления после успешного удаления

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Locations.objects.get(pk=pk)

    def delete(self, request, *args, **kwargs):
        logger.info(f'Deleted loc {self.kwargs['pk']}')
        return super().delete(request, *args, **kwargs)


class EditOrgView(LoginRequiredMixin, UpdateView):
    model = Organisation
    template_name = 'edit_org.html'
    form_class = OrgForm  # Используем вашу собственную форму

    # Указываем URL для перенаправления после успешного обновления
    success_url = reverse_lazy('edit-choice')

    # Переопределяем метод get_object(), чтобы получить объект Organisation для редактирования
    def get_object(self, queryset=None):
        return Organisation.objects.get(pk=self.kwargs['pk'])

    # Переопределяем метод form_valid(), чтобы добавить дополнительную логику при успешном обновлении формы
    def form_valid(self, form):
        # Ваша дополнительная логика
        logger.debug(f'Edited org {self.kwargs['pk']}')
        return super().form_valid(form)


class EditLocView(LoginRequiredMixin, UpdateView):
    model = Locations
    template_name = 'edit_loc.html'
    form_class = LocationsForm  # Используем вашу собственную форму

    # Указываем URL для перенаправления после успешного обновления
    success_url = reverse_lazy('edit-choice')

    # Переопределяем метод get_object(), чтобы получить объект Organisation для редактирования
    def get_object(self, queryset=None):
        return Locations.objects.get(pk=self.kwargs['pk'])

    # Переопределяем метод form_valid(), чтобы добавить дополнительную логику при успешном обновлении формы
    def form_valid(self, form):
        # Ваша дополнительная логика
        logger.debug(f'Edited loc {self.kwargs['pk']}')
        return super().form_valid(form)


class AddLocMedia(LoginRequiredMixin, FormView):
    template_name = 'add_loc_media.html'
    success_url = reverse_lazy("edit-choice")  # Подставьте ваш URL
    org_form_class = LocationMediaForm
    model = LocationMedia
    fields = ['image', 'description', ]

    def get_form_class(self):
        return LocationMediaForm

    def form_valid(self, form):
        logger.debug("Valid form for add loc media")
        loc_id = self.kwargs['pk']
        loc = Locations.objects.get(pk=loc_id)  # Получаем объект Org по org_id
        form.instance.location = loc
        form.save()  # Сохраняем форму
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.info(f"Invalid form for add loc media. Error: {form.error}")
        return super().form_invalid(form)


class EditLocMediaView(LoginRequiredMixin, UpdateView):
    model = LocationMedia
    template_name = 'edit_loc_media.html'
    form_class = LocationMediaForm  # Используем вашу собственную форму
    success_url = reverse_lazy('edit-choice')

    def get_object(self, queryset=None):
        return LocationMedia.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        logger.debug(f'Edited media-form')
        return super().form_valid(form)


class DelLocMediaView(LoginRequiredMixin, DeleteView):
    model = LocationMedia
    template_name = 'confirm_delete_loc_media.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('edit-choice')  # URL для перенаправления после успешного удаления

    def get_object(self, queryset=None):
        return LocationMedia.objects.get(pk=self.kwargs.get('pk'))

    def delete(self, request, *args, **kwargs):
        logger.info(f'Deleted media {self.kwargs.get('pk')}')
        return super().delete(request, *args, **kwargs)

        """Какие нужны страницы? 
        1. Добавление локации к орге
        Ответ gpt 3:23 заслуживает внимания. Вынести атрибуты в 2 классе и наследовать на выбор вместе с миксинами и view"""
