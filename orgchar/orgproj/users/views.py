from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import DetailView, UpdateView
import logging
from users.form import UserProfileForm, ProfileUserForm, UserPasswordChangeForm
from users.models import UserProfile

import smtplib

# Create your views here.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CustomLogin(LoginView):
    template_name = "login.html"
    # success_url = redirect('map')
    # success_url = reverse_lazy('map')
    success_url = reverse_lazy('orgs:edit-choice')
    redirect_authenticated_user = False  # Change to True after debug


def logout_view(request):
    logout(request)
    # Перенаправление на главную страницу после выхода из системы
    return redirect('map')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"  # Убедитесь, что файл шаблона существует с этим именем
    success_url = reverse_lazy(
        'profile')  # Замените 'profile_detail_view' на имя вашего URL-маршрута для просмотра профиля

    def get_object(self, queryset=None):
        # Убедитесь, что пользователь может редактировать только свой профиль
        return self.request.user.profile

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму."""
        kwargs = super(UserProfileUpdateView, self).get_form_kwargs()
        kwargs.update()
        return kwargs


class UserProfileView(DetailView):
    model = User
    template_name = "profile.html"

    # context_object_name = "users_data"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.object

        users_data = {
            'email': user.username,
            'name': user.profile.name,
            'surname': user.profile.surname,
            'phone': user.profile.phone,
        }

        context['users_data'] = users_data

        return context


# def registration_view(request):
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#
#             profile = UserProfile(profile_id=user.pk)
#             profile.save()
#
#             login(request, user)
#             messages.success(request, "Registration is done")
#
#             return redirect('about')
#
#         else:
#             return render(request, 'registration.html', context={"form": form})
#     else:
#         form = CustomUserForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'registration.html', context)


def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            profile = UserProfile(profile_id=user.pk)
            profile.save()

            login(request, user)
            messages.success(request, "Registration is done")

            return redirect('map')

        else:
            return render(request, 'registration.html', context={"form": form})
    else:
        form = UserCreationForm()
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
        return reverse_lazy('users:profile', args=[self.request.user.pk])

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
