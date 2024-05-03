from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeDoneView
from django.urls import path, include, reverse_lazy

from orgproj import settings
from users import views
from users.views import CustomResetView

urlpatterns = ([
    path('login/', views.CustomLogin.as_view(), name="login"),
    path('profile1/', views.UserProfileView.as_view(), name='profile1'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('profile/edit/', views.UserProfileUpdateView.as_view(), name='profile_edit'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view, name="registration_view"),

    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="password_change_done.html"),
         name="password_change_done"),

    path('password-reset/',
         CustomResetView.as_view(

         ),
         name='password_reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="pass_reset_done.html"),
         name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name="pass_reset_confirm.html",
        success_url=reverse_lazy('password_reset_complete')),
         name='password_reset_confirm'),

    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="pass_reset_complete.html"),
         name='password_reset_complete'),

])