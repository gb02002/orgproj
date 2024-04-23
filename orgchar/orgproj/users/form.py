from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.forms import ModelForm

from users.models import UserProfile


class CustomUserForm(UserCreationForm):
    username = forms.EmailField(max_length=50, min_length=6, label='Email')
    password1 = forms.CharField(min_length=6, max_length=30, label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=6, max_length=30, label='confirm password', widget=forms.PasswordInput)

    class Meta:
        fields = ("username", "password1", "password2")
        # field_classes = {"username": UsernameField}


# class ProfileForm(forms.Form):
#     name = forms.CharField(max_length=20, min_length=2, label="Name")
#     surname = forms.CharField(max_length=30, min_length=2, label="Surname")
#     phone = fo


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["name", "surname", "phone"]


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))