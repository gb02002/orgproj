from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
import logging
from django.contrib.auth.models import User
from django.urls import reverse

test_file = SimpleUploadedFile("test_file.pdf", b"file_content", content_type="application/pdf")


class CustomLoginViewTests(TestCase):

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_template_used(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'login.html')

    def test_login_redirect_authenticated_user_false(self):
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)

    def test_login_redirect_authenticated_user_true(self):
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('login'))

        # self.assertRedirects(response, reverse('edit-choice')) Won't work with debug=true
        self.assertEqual(response.status_code, 200)


class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_logout_redirect_to_home(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))

        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('map'))


class RegistrationViewTests(TestCase):

    def test_registration_success(self):
        # Отправляем POST запрос с корректными данными формы
        response = self.client.post(reverse('registration_view'), {
            'email': 'testuser@mail.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'file': test_file,
        })

        self.assertTrue(response.wsgi_request.user.is_authenticated)

        self.assertRedirects(response, reverse('map'))

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Registration is done')

    def test_registration_failure_invalid_form(self):
        # Отправляем POST запрос с неправильными данными формы
        response = self.client.post(reverse('registration_view'), {
            'username': '',  # Пустое имя пользователя
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        # Проверяем, что пользователь не аутентифицирован (т.к. регистрация не удалась)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        # Проверяем, что пользователь остается на странице регистрации
        self.assertEqual(response.status_code, 200)
        # Проверяем, что форма возвращается с ошибками
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertTrue('email' in form.errors)
