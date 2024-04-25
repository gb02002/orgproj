import redis
import psycopg2
import ujson
import os
import sys

# Добавляем путь к папке orgproj в список путей Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'orgproj')))

# Теперь вы можете импортировать модуль settings из orgproj
from orgproj import settings

# Подключение к Redis
redis_host = os.getenv(settings.REDIS_HOST)
redis_port = settings.REDIS_PORT
# redis_port = os.getenv(settings.REDIS_PORT)
redis_db = 0
redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

# PostgreSQL connection
# pg_host = 'localhost'
# pg_port = settings.POSTGRES_PORT
# pg_db = os.getenv(settings.POSTGRES_DBNAME)
# pg_user = os.getenv(settings.POSTGRES_USER)
# pg_password = os.getenv(settings.POSTGRES_USER_PASSWORD)

# pg_conn = psycopg2.connect(host=pg_host, port=pg_port, database=pg_db, user=pg_user, password=pg_password)


pg_conn = psycopg2.connect(f'dbname=ccharity16 user=postgres host=localhost port=5433 password=1111')
pg_cursor = pg_conn.cursor()

redis_key_pattern = 'web_stat:*'

# SQL запрос для вставки данных

insert_query = ("INSERT INTO web_stats (time_stamp, session_id, path_info, response_code, time_for_response, "
                "user_agent, ip_addr, referer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

# Проход по ключам в Redis
for key in redis_conn.scan_iter(match=redis_key_pattern):
    value = redis_conn.get(key)
    if value:
        decoded_value = value.decode('utf-8').strip()
        clean_data = tuple(ujson.loads(decoded_value))

        pg_cursor.execute(insert_query, clean_data)
        pg_conn.commit()
        redis_conn.delete(key)
# Закрытие соединений
pg_cursor.close()
pg_conn.close()
