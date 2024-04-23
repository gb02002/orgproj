from rest_framework import serializers
from orgs.models import Locations, Organisation, FilterforLocation
import logging

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARNING)


class BoundsSerializer(serializers.Serializer):
    """Serializer for retrieving users coordinates """
    bounds_dict = serializers.DictField()

    def validate(self, data):
        bounds_dict = {"north": 54.0270141, "south": 50.0819879, "west": 2.90730629, "east": 7.6831597}

        data = data['bounds_dict']

        # Create a list of boundaries
        min_latitude = bounds_dict["south"]
        max_latitude = bounds_dict["north"]
        min_longitude = bounds_dict["west"]
        max_longitude = bounds_dict["east"]

        for coord, value in data.items():
            if value is None or not isinstance(value, (int, float)):
                raise serializers.ValidationError(
                    f"Invalid value for {coord}. Must be a number. Happens in {coord} with {value}")

        if not (min_latitude <= data["south"] <= max_latitude) or not (min_latitude <= data["north"] <= max_latitude):
            raise serializers.ValidationError("Latitude is out of bounds")

        if not (min_longitude <= data["west"] <= max_longitude) or not (min_longitude <= data["east"] <= max_longitude):
            raise serializers.ValidationError("Longitude is out of bounds")

        logger.debug(f"Serialized coords: {data}")
        return data


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

