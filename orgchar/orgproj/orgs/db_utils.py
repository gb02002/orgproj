from typing import Union

from django.db.models import QuerySet
from orgs.models import Locations
import logging
from django.contrib.gis.geos import Polygon

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARNING)


def query_rectangular_orm(coords: dict) -> list[QuerySet[Locations]]:
    """Gets set of point and returns location list. Method 2.1"""
    logger.debug(f"В бд пришли такие координаты: {coords}")

    rectangle = Polygon.from_bbox((coords['west'], coords['south'], coords['east'], coords['north']))

    query_set = Locations.loc_man.get_locations_within(rectangle)

    logger.debug(f"Бд отдала вот такие локации {query_set.count()}, {query_set.values_list()}")

    return list(query_set)


def get_full_data(loc_id: list[int]) -> Union[QuerySet['Locations'], None]:
    """Currently is not used"""
    """retrive info about location:
        title, address, hours, org_desc, mail, phone, web, bank, tikkie"""

    location_info = Locations.loc_man.full_data_map(loc_id)

    return location_info
