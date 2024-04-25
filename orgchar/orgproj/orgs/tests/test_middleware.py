import logging
from importlib import import_module
from unittest.mock import Mock
from django.contrib.sessions.backends.db import SessionStore
from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User

from orgproj import settings
from orgs.middleware import CustomMiddlewareToken
logger = logging.getLogger(__name__)
# logger.setLevel(logging.WARNING)
logger.setLevel(logging.DEBUG)


class CustomMiddlewareTokenTestCase(TestCase):
    """
    Basically a type of integrity test
    dunno how to work with passing mock to _get_response and parsing TypeNone after RequestFactory fuck it
    """
    def test_process_view_without_edit_choice(self):
        """"    works   """
        mock_get_response = Mock()

        request = RequestFactory().get('/')

        session = SessionStore()

        request.session = session

        middleware = CustomMiddlewareToken(mock_get_response)
        middleware(request)

        # Проверяем, что в сессию не добавлен токен
        self.assertNotIn('edit_token', request.session)

    def test_token_middleware_no_token(self):
        """"    works   """
        # Создаем клиент и пользователя
        user = User.objects.create_user(username='username', password='password')
        client = Client()

        # Авторизуем пользователя
        client.login(username='username', password='password')

        # Делаем запрос к нужному URL
        response = client.get(reverse('add-org-1'))

        # Проверяем, что получили редирект
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект
        self.assertEqual(response.url, '/lo/for_orgs/edit-choice/')

        # def test_token_middleware_no_token(self):

    def test_token_middleware_no_token_edit_choice(self):
        """"    works   """
        User.objects.create_user(username='username', password='password')
        client = Client()
        client.login(username='username', password='password')

        response = client.get(reverse('edit-choice'))

        self.assertTrue(response.request["PATH_INFO"].endswith('/lo/for_orgs/edit-choice/'))
        # self.assertIn('edit_token', response.session)

    def test_token_middleware_with_token(self):
        """"    works   """
        User.objects.create_user(username='username', password='password')
        client = Client()
        client.login(username='username', password='password')

        client.get(reverse('edit-choice'))
        response = client.get(reverse('add-org-1'))

        self.assertEqual(response.request["PATH_INFO"], '/lo/for_orgs/edit-choice/add-org-1/')
