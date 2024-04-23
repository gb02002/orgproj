import logging

from django.contrib.gis.geos import Point
from django.http import QueryDict
from django.test import TestCase
from rest_framework import serializers
from rest_framework.utils import json

from orgs.models import Locations, Organisation, FilterforLocation, LocationMedia
from orgs.serializers import BoundsSerializer, LocationIdsSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
# logger.setLevel(logging.DEBUG)


class BoundsSerializerTest(TestCase):
    """Tests from old proj"""

    def test_valid_data(self):
        data = {"north": 52, "south": 52, "west": 5, "east": 4}
        serializer = BoundsSerializer(data={'bounds_dict': data})
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {"south": 25, "east": 1.6}
        serializer = BoundsSerializer(data={'bounds_dict': data})

        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data={'bounds_dict': data})

    def test_invalid_data_type(self):
        data = {"south": 25, "east": 1.6, "north": 'ser', "west": 12}
        serializer = BoundsSerializer(data={'bounds_dict': data})

        with self.assertRaises(serializers.ValidationError):
            serializer.validate(data={'bounds_dict': data})


class LocationIdsSerializerTestCase(TestCase):
    def test_to_internal_value(self):
        serializer = LocationIdsSerializer()
        query_params = QueryDict('location_ids=1,2,3')

        internal_value = serializer.to_internal_value(query_params)

        self.assertEqual(internal_value['location_ids'], [1, 2, 3])

    def test_to_internal_value_empty_location_ids(self):
        serializer = LocationIdsSerializer()
        query_params = QueryDict('')

        internal_value = serializer.to_internal_value(query_params)

        self.assertEqual(internal_value['location_ids'], [])

    def test_to_internal_value_non_integer_location_ids(self):
        serializer = LocationIdsSerializer()
        query_params = QueryDict('location_ids=a,b,c')

        internal_value = serializer.to_internal_value(query_params)

        self.assertEqual(internal_value['location_ids'], [])