# This is middleware for analytics
import ujson
import os
from datetime import datetime
from typing import NamedTuple, Tuple
import uuid
from uuid_extensions import uuid7str
import redis
from django.conf import settings
import time
import logging
from redis import RedisError

from users.tasks import alert_error_mail

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.WARNING)
time_to_live = 60 * 3


# logger.setLevel(logging.WARNING)

class WebStatistics(NamedTuple):
    time_stamp: str
    session_id: str
    path_info: str
    response_code: int
    time_for_response: float
    User_Agent: str = ''
    ip_addr: str = ''
    referer: str = ''

    def __str__(self):
        return (
            f"WebStats(time_stamp={self.time_stamp}), session_id={self.session_id}, path_info={self.path_info}, "
            f"response_code={self.response_code}, time_for_response={self.time_for_response}, "
            f"User_Agent={self.User_Agent}), ip_addr={self.ip_addr}), referer={self.referer})")


class StatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        try:
            redis_host = os.getenv('REDIS_HOST', settings.REDIS_HOST)
            redis_port = os.getenv('REDIS_PORT', settings.REDIS_PORT)
            redis_decode_responses = os.getenv('REDIS_DECODE_RESPONSES', settings.REDIS_DECODE_RESPONSES)
            self.rdc = redis.Redis(host=redis_host, port=redis_port, decode_responses=redis_decode_responses)

            self.start_time = time.monotonic()
        except RedisError as e:
            logger.warning(f"No connection with redis in middleware: {e}")
            alert_error_mail(e)

    def __call__(self, request):
        # request part
        response = self.get_response(request)
        # response
        if 'lo/api' in request.path_info:
            return response
        if self.rdc:
            try:
                web_stats_result = self.collect_data(request, response)
                key, value = web_stats_result
                self.rdc.set(key, value, ex=time_to_live)

            except RedisError as e:
                logger.error(f'Not possible to redis set: {e}')
                return response
            except (AttributeError, KeyError) as e:
                logger.error(f'no attr in request(apparently): {e}')
            except Exception as e:
                logger.error(f'parsing webstats error: {e}')
                alert_error_mail(e)
            finally:
                return response
        return response

    def collect_data(self, request, response) -> Tuple[str, str]:
        unique_identifier = uuid.uuid4()
        ip_address = request.META.get('REMOTE_ADDR', '')
        referer = request.META.get('HTTP_REFERER', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        handling_time = time.monotonic() - self.start_time

        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key

        web_stat = WebStatistics(
            time_stamp=uuid7str(),
            session_id=session_id,
            path_info=request.path_info,
            response_code=response.status_code,
            time_for_response=handling_time,
            User_Agent=user_agent,
            ip_addr=ip_address,
            referer=referer
        )

        logger.warning(web_stat)

        web_stat_json = ujson.dumps(web_stat)
        key = f'web_stat:{unique_identifier}'

        return key, web_stat_json
