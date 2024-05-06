from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from users.models import UserProfile
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']
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
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class UploadFileForm(forms.Form):
    file = forms.FileField(label="PDF document", required=True)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        logger.debug(f"email: {email}")
        if not email:
            raise forms.ValidationError("This field is required.")
        return email

    def clean_document_file(self):
        document_file = self.cleaned_data.get('document_file')

        if not document_file:
            return None

        allowed_types = ['application/pdf']  # Добавьте другие разрешенные типы файлов, если нужно
        if document_file.content_type not in allowed_types:
            raise ValidationError('Only PDF files are allowed.')

        max_size = 10 * 1024 * 1024
        if document_file.size > max_size:
            raise ValidationError('File size cannot exceed 10 MB.')

        return document_file
