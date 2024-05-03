from rest_framework import serializers
from orgs.models import Locations, Organisation, FilterforLocation
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.WARNING)


class BoundsSerializer(serializers.Serializer):
    """Serializer for retrieving users coordinates """
    bounds_dict = serializers.DictField()

    def validate(self, data):
        bounds_dict = {"north": 54.0270141, "south": 50.0819879, "west": 2.90730629, "east": 7.6831597}

        data = data['bounds_dict']

        south = data.get('south', None)
        north = data.get('north', None)
        west = data.get('west', None)
        east = data.get('east', None)

        if not all(isinstance(val, (int, float)) for val in [south, north, west, east]):
            raise serializers.ValidationError("Coordinates must be numbers.")

        if south is not None and north is not None:
            if south > north:
                south, north = north, south
            south = max(south, 50.0819879)  # Минимальная южная граница
            north = min(north, 54.0270141)  # Максимальная северная граница

        if west is not None and east is not None:
            if west > east:
                west, east = east, west
            west = max(west, 2.90730629)  # Минимальная западная граница
            east = min(east, 7.6831597)  # Максимальная восточная граница

        logger.debug(f"Serialized coords: {data}")
        return {
            'south': south,
            'north': north,
            'west': west,
            'east': east
        }


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['organisation', 'title', 'desc', 'mail', 'phone', 'web']


class LocInfoSerializer(serializers.ModelSerializer):
    related_org = OrganisationSerializer(read_only=True)

    class Meta:
        model = Locations
        fields = ['location', 'location_name', 'address', 'open_hours', 'filter_id', 'related_org']


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterforLocation
        fields = ['filter_id', 'filter_name']


class LocationIdsSerializer(serializers.Serializer):
    """query-params[int] -> list[int]"""
    location_ids = serializers.ListField(child=serializers.IntegerField())

    def to_internal_value(self, data):
        logger.debug("Converting query params to internal value in LocationSerializer")
        # Создаем копию объекта QueryDict
        mutable_data = data.copy()

        # Получаем значение location_ids из копии и преобразуем его
        location_ids_str = mutable_data.get('location_ids', '')
        mutable_data['location_ids'] = [int(id) for id in location_ids_str.split(',') if id.isdigit()]

        # Возвращаем обновленный объект QueryDict
        return mutable_data

