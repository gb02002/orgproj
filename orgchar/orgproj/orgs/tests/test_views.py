import logging
from collections import OrderedDict
from unittest.mock import patch

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse
from faker.utils.text import slugify
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from django.test import override_settings
from rest_framework.utils import json

from orgs.models import Locations, Organisation, FilterforLocation, LocationMedia
from orgs.views import GetFiltersApiView

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
# logger.setLevel(logging.DEBUG)


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class CustomTestCase(TestCase):
    """Custom realization of testcase with extra setup"""

    def setUp(self):
        self.client_api = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client_api.login(username='testuser', password='password')

        self.client.login(username='testuser', password='password')

        # self.token = Token.objects.create(user=self.user)
        #
        # # Добавляем токен аутентификации в каждый запрос
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.org_bounds1 = Organisation.objects.create(
            title="Test Organization1",
            desc="Test Description",
            mail="test2@example.com",
            phone="1234567849",
            web="http://examp1le.com",
            agent=self.user,
        )

        self.filter1 = FilterforLocation.objects.create(filter_name="Test Filter")

        self.loc_bounds = Locations.objects.create(
            location_name="Test Location",
            related_org=self.org_bounds1,
            address="Test Address",
            open_hours="Test Hours",
            point=Point(6.945807998798116, 52.287899734023104),
            filter=self.filter1
        )
        # Настройка данных, применяемая ко всем тестам в модуле
        self.org2 = Organisation.objects.create(title="Test Organization2",
                                                desc="Test Description",
                                                mail="test@example.com",
                                                phone="123456789",
                                                web="http://example.com",
                                                agent=self.user, )

        self.org3 = Organisation.objects.create(title="Test Organization3",
                                                desc="Test Description2",
                                                mail="test1@example.com",
                                                phone="123456781",
                                                web="http://example1.com",
                                                agent=self.user, )

        super().setUp()

    def tearDown(self):
        # Здесь вы можете выполнять любые действия, которые нужно выполнить после каждого теста
        Locations.objects.all().delete()
        Organisation.objects.all().delete()
        FilterforLocation.objects.all().delete()
        LocationMedia.objects.all().delete()
        self.user.delete()

        super().tearDown()


class LocationBoundsFilterViewTest(CustomTestCase):
    middle_coords = {"north": 51, "south": 52, "west": 5, "east": 5.3}
    correct_coords = {'north': 52.337176750268554, 'south': 52.0840783775989,
                      'west': 6.220497939193819, 'east': 7.046593195331092}
    correct_coords_no_content = {'north': 51.337176750268554, 'south': 51.0840783775989,
                                 'west': 6.220497939193819, 'east': 7.046593195331092}
    out_of_scope_coords = {"north": 30, "south": 28, "west": 4, "east": 3.5}
    null_coords = {"north": 1, "south": 0, "west": 1, "east": 2}
    url = reverse('filter_map.api')

    def test_valid_post_request(self):
        """Тестирование корректного POST-запроса с правильными параметрами"""
        bounds_data = {'bounds': self.correct_coords}

        response = self.client_api.post(self.url, bounds_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'test_valid_post_request fail')

    def test_invalid_json_format(self):
        """Тестирование некорректного формата JSON в параметре bounds"""
        response = self.client_api.post(self.url, {'bounds': {'"south": 51.797178820141646, "west": 5, "east": 5.3'}},
                                        format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'test_invalid_json_format fail')

    def test_outer_coords(self):
        """Коодинаты, сильно далекие от рабочей области"""
        bounds_data = {'bounds': self.out_of_scope_coords}

        response = self.client_api.post(self.url, bounds_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'test_outer_coords fail')

    def test_missing_bounds_parameter(self):
        # Тестирование отсутствия параметра bounds в GET-запросе
        # with self.assertRaises(TypeError):
        #     response = self.client.post(self.url, {}, format='json')
        response = self.client_api.post(self.url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'test_missing_bounds_parameter fail')

    def test_no_content(self):
        """Коодинаты, сильно далекие от рабочей области"""
        bounds_data = {'bounds': self.correct_coords_no_content}

        response = self.client_api.post(self.url, bounds_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'test_no_content fail')


class OrganisationListViewTests(CustomTestCase):
    def setUp(self):
        super().setUp()

    def test_organisation_list_view(self):
        # Проверяем, что страница загружается успешно
        response = self.client_api.get(reverse('organisation_list_filtered'))
        self.assertEqual(response.status_code, 200, "Не 200")

        # Получаем объект page_obj из контекста ответа
        page_obj = response.context['page_obj']

        organisations_on_page = [repr(i) for i in page_obj]
        expected_organisations = [
            repr(self.org_bounds1),
            repr(self.org2),
            repr(self.org3)
        ]

        self.assertQuerysetEqual(
            organisations_on_page,
            expected_organisations,
            ordered=False,
            msg="Неправильные организации на странице"
        )

    # def test_get_params_extraction(self):
    #     """Currently not in use"""
    #     # Создаем запрос с параметром filter_id
    #     response = self.client.get(reverse('organisation-list'), {'filter_id': '1,2,3'})
    #
    #     # Проверяем, что метод get_params корректно извлекает параметры из запроса
    #     self.assertEqual(response.context['params'], [1, 2, 3])


class LocationListApiViewTests(APITestCase):
    def test_get_locations_success(self):
        # Создаем тестовые данные
        location_ids = [1]
        # locations_data = [{'id': 1, 'name': 'Location 1'}, {'id': 2, 'name': 'Location 2'},
        #                   {'id': 3, 'name': 'Location 3'}]
        locations_data1 = [OrderedDict({'location': 1, 'location_name': 'Test Location', 'address': 'Test Address',
                                        'open_hours': 'Test Hours', 'filter_id': 1, 'related_org':
                                            OrderedDict({'organisation': 1, 'title': 'Test Organization1',
                                                         'desc': 'Test Description', 'mail': 'test2@example.com',
                                                         'phone': '1234567849', 'web': 'http://examp1le.com'})})]

        # Мокаем метод full_data_map, чтобы он возвращал тестовые данные
        with patch.object(Locations.loc_man, 'full_data_map', return_value=locations_data1):
            # Отправляем запрос GET на URL вашего view
            url = reverse('list_loc.api')
            response = self.client.get(url, data={'location_ids': ','.join(map(str, location_ids))})

            response_data = response.json()

            # Проверяем, что запрос завершился успешно и данные верны
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response_data['result'][0], locations_data1[0])

    def test_get_locations_no_content(self):
        # Отправляем запрос GET без передачи location_ids
        url = reverse('list_loc.api')
        response = self.client.get(url)

        # Проверяем, что возвращается код статуса HTTP 400 (некорректный запрос)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_locations_no_locations_found(self):
        # Создаем тестовые данные
        location_ids = [4, 5, 6]

        # Мокаем метод full_data_map, чтобы он возвращал пустой список
        with patch.object(Locations.loc_man, 'full_data_map', return_value=[]):
            # Отправляем запрос GET на URL вашего view
            url = reverse('list_loc.api')
            response = self.client.get(url, data={'location_ids': ','.join(map(str, location_ids))})

            # Проверяем, что возвращается код статуса HTTP 204 (нет содержимого)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GetFiltersApiViewTests(CustomTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def tearDown(self):
        pass

    @patch('orgs.views.FilterforLocation.objects.all')
    def test_get_filters_success(self, mock_filters_all):
        # Мокаем вызов объекта фильтров, чтобы вернуть фильтры
        mock_filters_all.return_value = [{'filter_id': 1, 'filter_name': 'Filter 1'},
                                         {'filter_id': 2, 'filter_name': 'Filter 2'},
                                         {'filter_id': 3, 'filter_name': 'Filter 3'}]

        # Создаем запрос GET к представлению
        request = self.factory.get('filterapi')
        response = GetFiltersApiView.as_view()(request)

        # Проверяем, что данные фильтров передаются в ответе
        expected_data = [{'filter_id': 1, 'filter_name': 'Filter 1'},
                         {'filter_id': 2, 'filter_name': 'Filter 2'},
                         {'filter_id': 3, 'filter_name': 'Filter 3'}]

        # Получите данные из JsonResponse и сравните их с ожидаемыми данными
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, expected_data)  # Сравните JSON-ответ с ожидаемыми данными

    @patch('orgs.views.FilterforLocation.objects.all')
    def test_get_filters_no_filters(self, mock_filters_all):
        # Мокаем вызов объекта фильтров, чтобы вернуть пустой список
        mock_filters_all.return_value = []

        # Создаем запрос GET к представлению
        request = self.factory.get('filterapi')
        response = GetFiltersApiView.as_view()(request)

        # Проверяем, что код статуса ответа - 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что в ответе нет данных фильтров
        self.assertEqual(response.data, None)


class OrganisationDetailViewTest(CustomTestCase):

    def setUp(self):
        # self.other_test_instance = CustomTestCase()
        # self.other_test_instance.setUp()
        super().setUp()
        self.factory = RequestFactory()
        self.slug = slugify(self.org_bounds1.title)  # Создаем slug из title с помощью slugify
        self.view_url = reverse('organisation-detail',
                                kwargs={'pk': self.org_bounds1.organisation, 'slug': self.slug})

    def test_detail_view_returns_correct_template(self):
        response = self.client_api.get(self.view_url)
        self.assertTemplateUsed(response, 'detail_org.html')

    def test_detail_view_returns_correct_context(self):
        response = self.client_api.get(self.view_url)
        expected_locs = [repr(self.loc_bounds)]
        actual_locs = [repr(i) for i in response.context['locations']]
        self.assertEqual(response.context['org'], self.org_bounds1)
        self.assertQuerysetEqual(actual_locs, expected_locs)
        self.assertEqual(response.context['title'], "Page of Test Organization1")

    # def test_cache_page_decorator_used(self):
    #     other_test_instance = self.other_test_instance
    #     request = self.factory.get(self.view_url)
    #     view_instance = OrganisationDetailView.as_view()
    #     response = view_instance(request, pk=other_test_instance.org_bounds1.pk, slug=self.slug)
    #     self.assertTrue(response.has_header('Expires'))


class ChoiceEditViewTest(CustomTestCase):
    def setUp(self):
        super().setUp()
        self.view_url = reverse('edit-choice')

    def test_correct_context(self):
        response = self.client.get(self.view_url)
        result_agent = response.context_data['orgs'][0].agent

        expected_orgs = [repr(self.org_bounds1), repr(self.org2), repr(self.org3)]
        actual_orgs = [repr(i) for i in response.context_data.get('orgs', [])]

        self.assertEqual(result_agent, self.user)
        self.assertQuerysetEqual(expected_orgs, actual_orgs, ordered=False)

    def test_no_context_data(self):
        User.objects.create_user(username='testuser1', password='somepass')
        self.client1 = Client()
        self.client1.login(username='testuser1', password='somepass')
        response = self.client1.get(self.view_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('orgs', response.context_data, msg="orgs should be present in context")
        self.assertFalse(response.context_data['orgs'].exists(), msg="orgs queryset should be empty")

    def test_correct_token_generation(self):
        self.client.get(self.view_url)

        self.assertIn('edit_token', self.client.session)
        # Теперь проверяем, что токен имеет правильный формат или что он сгенерирован правильно
        token = self.client.session['edit_token']
        self.assertTrue(token.isalnum(), "Token should contain only alphanumeric characters")
        self.assertEqual(len(token), 32, "Token should have length of 32 characters")

    def test_LoginRequiredMixin(self):
        response = Client().get(self.view_url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn('/login/', response.url)

    def test_authenticated_access(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)


class f(CustomTestCase):
    pass
