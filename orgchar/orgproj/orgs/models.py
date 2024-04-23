from typing import Union

from django.contrib.auth.models import User
from django.contrib.gis.geos import Polygon
from django.core.validators import URLValidator
from django.db import models
from django.db.models import Manager, QuerySet
from django.contrib.gis.db import models


# Create your models here.

class Organisation(models.Model):
    """Org model"""

    organisation = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    desc = models.TextField(blank=True)
    mail = models.EmailField(unique=True)
    phone = models.CharField(unique=True, max_length=20)
    web = models.URLField(unique=True, validators=[URLValidator(schemes=['http', 'https'])])
    agent = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orgs', default=None, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Организации'
        verbose_name_plural = 'Организации'

    objects = Manager()


class FilterforLocation(models.Model):
    filter_id = models.AutoField(primary_key=True)
    filter_name = models.CharField(max_length=50, unique=True)

    objects = Manager()

    def __str__(self):
        return self.filter_name


class LocationsManager(models.Manager):
    def get_locations_within(self, rectangle: Polygon, filters=None) -> QuerySet['Locations']:
        if filters:
            return self.filter(point__within=rectangle, filter_id__in=filters).values('location', 'location_name',
                                                                                      'point', 'filter_id')
        return self.filter(point__within=rectangle)

    def full_data_map(self, loc_ids: list[int]) -> Union[QuerySet['Locations'], None]:
        """Retrieve location data with related organization data using select_related."""
        try:
            info = self.select_related('related_org').filter(pk__in=loc_ids)
            return info
        except self.model.DoesNotExist:
            return None


class Locations(models.Model):
    location = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=255, verbose_name="name")
    related_org = models.ForeignKey(Organisation, on_delete=models.PROTECT, related_name="locations")
    address = models.CharField(max_length=255, unique=True)
    open_hours = models.CharField(max_length=100)
    point = models.PointField(spatial_index=True, srid=4326)
    filter = models.ForeignKey(FilterforLocation, on_delete=models.PROTECT, related_name="locations_filtered",
                               db_index=True, verbose_name="filter")

    objects = Manager()
    loc_man = LocationsManager()

    def __str__(self):
        return '{} - {}'.format(self.location_name, self.address)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class LocationMedia(models.Model):
    media_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, related_name="media")
    image = models.ImageField(upload_to='location_media/')
    description = models.TextField(blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"Media {self.media_id} for {self.location.location_name}"

    class Meta:
        verbose_name = 'Медиа-файл'
        verbose_name_plural = 'Медиа-файлы'
