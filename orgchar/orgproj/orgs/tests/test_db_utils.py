import logging
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import RequestFactory, Client
from django.contrib.gis.geos import Point
from django.test import TestCase

from orgs.db_utils import query_rectangular_orm
from orgs.models import Locations, FilterforLocation, Organisation

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
# logger.setLevel(logging.DEBUG)


class QueryRectangularORMTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

        self.org_bounds1 = Organisation.objects.create(
            title="Test Organization1",
            desc="Test Description",
            mail="test2@example.com",
            phone="1234567849",
            web="http://examp1le.com",
            agent=self.user,
        )

        self.filter1 = FilterforLocation.objects.create(filter_name="Test Filter")

    def test_query_rectangular_orm(self):
        Locations.objects.create(
            location_name="Test Location1",
            related_org=self.org_bounds1,
            address="Test Address1",
            open_hours="Test Hours1",
            point=Point(6.945807998798116, 53.287899734023104),
            filter=self.filter1
        )

        Locations.objects.create(
            location_name="Test Location2",
            related_org=self.org_bounds1,
            address="Test Address2",
            open_hours="Test Hours2",
            point=Point(6.945807998798116, 54.287899734023104),
            filter=self.filter1
        )

        Locations.objects.create(
            location_name="Test Location3",
            related_org=self.org_bounds1,
            address="Test Address3",
            open_hours="Test Hours3",
            point=Point(5.945807998798116, 50.287899734023104),
            filter=self.filter1
        )

        # Задаем координаты для поиска
        coords = {'west': 5, 'south': 51, 'east': 7, 'north': 55}

        # Получаем результат функции
        result = query_rectangular_orm(coords)

        # Проверяем, что результат содержит QuerySet
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertEqual(len(result), 2, 'one is out of bounds')

        # Проверяем, что каждый элемент в списке - это QuerySet Locations
        for instance in result:
            self.assertIsInstance(instance, Locations)