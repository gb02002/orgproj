import sys
import redis
import psycopg2
import ujson
import os
import logging

# Добавляем путь к папке orgproj в список путей Python

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

redis_key_pattern = 'web_stat:*'

insert_query = ("INSERT INTO web_stats (time_stamp, session_id, path_info, response_code, time_for_response, "
                "user_agent, ip_addr, referer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")


def connect_to_postgres():
    try:
        db_host = os.getenv('POSTGRES_HOST', 'localhost')
        db_port = os.getenv('POSTGRES_PORT', '5433')
        db_name = os.getenv('POSTGRES_DBNAME', 'ccharity16')
        db_user = os.getenv('POSTGRES_USER', 'postgres')
        db_password = os.getenv('POSTGRES_PASSWORD', '1111')

        logger.debug('Подключаемся к PostgreSQL')
        pg_conn = psycopg2.connect(
            f'dbname={db_name} user={db_user} host={db_host} port={db_port} password={db_password}')
        return pg_conn
    except psycopg2.Error as e:
        logger.error(f'Ошибка при подключении к PostgreSQL: {e}')
        sys.exit(1)


# Функция для подключения к Redis
def connect_to_redis():
    try:
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = os.getenv('REDIS_PORT', 6379)
        redis_db = 0

        logger.debug('Подключаемся к Redis')
        redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
        return redis_conn
    except redis.ConnectionError as e:
        logger.error(f'Ошибка при подключении к Redis: {e}')
        sys.exit(1)


# Функция для выполнения SQL запроса и вставки данных в PostgreSQL
def insert_data_to_postgres(pg_cursor, insert_query, clean_data):
    try:
        pg_cursor.execute(insert_query, clean_data)
        pg_cursor.connection.commit()
        logger.debug('Данные успешно вставлены в PostgreSQL')
    except psycopg2.errors.UndefinedTable as e:
        logger.error(f'Таблица не найдена в PostgreSQL: {e}')
    except psycopg2.Error as e:
        logger.error(f'Ошибка при вставке данных в PostgreSQL: {e}')


pg_conn = connect_to_postgres()
pg_cursor = pg_conn.cursor()
redis_conn = connect_to_redis()

# Проход по ключам в Redis
for key in redis_conn.scan_iter(match=redis_key_pattern):
    value = redis_conn.get(key)
    if value:
        decoded_value = value.decode('utf-8').strip()
        clean_data = tuple(ujson.loads(decoded_value))

        insert_data_to_postgres(pg_cursor, insert_query, clean_data)
        redis_conn.delete(key)

# Закрытие соединений
pg_cursor.close()
pg_conn.close()

logger.debug('Завершение')
