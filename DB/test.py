import pymysql.cursors
from contextlib import closing
import json
from config.config import DB_CONFIG

connection = pymysql.connect(
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database'],
    cursorclass=pymysql.cursors.DictCursor,
)


def update_user_info(user_id, **kwargs):
    if 'name' in kwargs.keys():
        value = kwargs['name']
        sql = "UPDATE testdb.users SET name = %s WHERE user_id = %s"

    if 'surname' in kwargs.keys():
        value = kwargs['surname']
        sql = "UPDATE testdb.users SET surname = %s WHERE user_id = %s"

    if 'lang' in kwargs.keys():
        value = kwargs['lang']
        sql = "UPDATE testdb.users SET lang = %s WHERE user_id = %s"

    # print(value)
    with connection.cursor() as cursor:
        cursor.execute(sql, (value, user_id))
        connection.commit()

    if connection.affected_rows() != 0:
        return 'updated'
    else:
        return 'not updated'


# print(update_user_info(19725615, name='sher'))
