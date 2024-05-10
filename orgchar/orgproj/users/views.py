from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, FormView
import logging
from users.form import UserProfileForm, ProfileUserForm, UserPasswordChangeForm, CustomUserCreationForm, UploadFileForm
from users.models import UserProfile

import smtplib

# Create your views here.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CustomLogin(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy('map')
    redirect_authenticated_user = False  # Change to True after debug

    def form_valid(self, form):
        """Valid form with redirect"""
        response = super().form_valid(form)
        next_url = self.request.GET.get('next')
        if next_url:
            return HttpResponseRedirect(next_url)
        return response


def logout_view(request):
    logout(request)
    return redirect('map')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"
    success_url = reverse_lazy('profile1')

    def get_object(self, queryset=None):
        # Убедитесь, что пользователь может редактировать только свой профиль
        return self.request.user.profile

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму."""
        kwargs = super(UserProfileUpdateView, self).get_form_kwargs()
        kwargs.update()
        return kwargs


# class UserProfileView(DetailView):
#     model = User
#     template_name = "profile1.html"
#
#     # context_object_name = "users_data"
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         user = self.object
#
#         users_data = {
#             'email': user.username,
#             'name': user.profile.name,
#             'surname': user.profile.surname,
#             'phone': user.profile.phone,
#         }
#
#         context['users_data'] = users_data
#
#         return context


def registration_view(request):
    """Regular reg_view. Email is username"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = user.email
                user.save()
                profile = UserProfile.objects.create(profile=user)

                profile.save()
                login(request, user)

                messages.success(request, "Registration is done")

                return redirect('map')
            except IntegrityError:
                messages.error(request, 'This email address is already in use.')
                return render(request, 'registration.html',
                              context={"form": form, "error_message": "This email address is already in use."})
        else:
            # Форма недействительна, отображаем ее с сообщениями об ошибках
            messages.error(request, 'Invalid form submission.')
            return render(request, 'registration.html', context={"form": form})
    else:
        form = CustomUserCreationForm(request.POST, request.FILES)
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'profile1.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('profile1')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "password_change_form.html"
    extra_context = {'title': "Изменение пароля"}


class CustomResetView(PasswordResetView):
    template_name = "pass_reset_form.html"
    email_template_name = "password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        fromaddr = 'baburin909@gmail.com'
        toaddrs = 'baburin-gb@yandex.ru'
        msg = 'Spam email Test1'

        username = 'baburin909@gmail.com'
        password = 'zplj skwn ibzp mgbx'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
        # sdfds

        # message = 'test2'
        # email = form.cleaned_data['email']
        # subject = "You got a message"
        # thoughts = "{} by {}".format(message, email)
        # recipients = ['baburin-gb@yandex.ru']
        # sender = 'baburin909@gmail.com'
        # send_mail(subject, thoughts, sender, recipients, fail_silently=False)
        response = super().form_valid(form)
        # Другие атрибуты, которые вы хотите вывести, могут быть получены из context

        # Вернем ответ (response), как это делает родительский класс
        return response


class UploadFileView(LoginRequiredMixin, FormView):
    form_class = UploadFileForm
    model = UserProfile
    template_name = 'UploadFileTemplate.html'
    success_url = reverse_lazy('profile1')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_invalid(self, form):
        error_message = f"Document upload failed due to the following errors: {form.errors}"
        logger.error(error_message)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # Получаем профиль пользователя
        profile = self.request.user.profile
        # Сохраняем файл в профиле пользователя
        profile.document_file = form.cleaned_data['file']
        profile.save()
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile3.html"

    # context_object_name = "users_data"

    def get_object(self, queryset=None):
        return self.request.user

    def get_queryset(self):
        return self.request.user.orgs.all().prefetch_related('locations__media')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        status_icon = user.profile.get_status_display_with_icon()

        users_data = {
            'email': user.username,
            'name': user.profile.name,
            'surname': user.profile.surname,
            'phone': user.profile.phone,
            'status_icon': status_icon,
            'status': user.profile.is_org_agent,
            'organisations': self.get_queryset()
        }

        context['users_data'] = users_data

        return context
