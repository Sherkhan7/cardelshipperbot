import pymysql.cursors
from contextlib import closing
import json
from config.config import DB_CONFIG


def get_connection():
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection


# mycursor = connection.cursor()

def insert_user(user_data):
    user_data.pop('code')
    user_data_field = tuple(user_data.keys())
    user_data_values = tuple(user_data.values())
    user_data_values_field = list()
    user_data_values_field.extend(['%s'] * len(user_data_values))
    user_data_values_field = tuple(user_data_values_field)

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO testdb.users ({','.join(user_data_field)}) VALUES ({','.join(user_data_values_field)})"
            cursor.execute(sql, user_data_values)
            connection.commit()

    # print(mycursor.rowcount, "record inserted.")

    return cursor.rowcount


def get_user(user_id):

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM testdb.users WHERE user_id = %s", user_id)
            record = cursor.fetchone()

    if record is None:
        return False

    return record
    """returns dict"""
    # record = dict()
    #
    # for i in range(len(columns)):
    #     record.update({columns[i]: value[i]})
    #
    # record['created_at'] = record['created_at'].strftime('%c')
    # record['updated_at'] = record['updated_at'].strftime('%c')
    #
    # print('rowcount: ', cursor.rowcount)
    # print('affected: ', connection.affected_rows())
    # mycursor.close()
    # return record


def get_user_json(user_id):
    user = get_user(user_id)

    return json.dumps(user, indent=4)


def check_user(user_id):
    user = get_user(user_id)

    if user:
        return True

    # connection.close()
    return False


def select_all():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM testdb.users')
        records = cursor.fetchall()

    print(cursor.rowcount)
    return records
    """ returns list of dicts"""

    # if records is None:
    #     return None
    #
    #
    #     # record = dict()
    #     # records_list = list()
    #     #
    #     # for record_item in records:
    #     #     for j in range(len(columns)):
    #     #         record.update({columns[j]: record_item[j]})
    #
    # # records['updated_at'] = records['updated_at'].strftime('%c')
    # # records['created_at'] = records['created_at'].strftime('%c')
    #
    # # records_list.append(record)
    # # record = {}
    # # return json.dumps(records_list, indent=4)


def update_user_info(user_id, **kwargs):
    if 'name' in kwargs.keys():
        value = kwargs['name']
        sql = "UPDATE testdb.users SET name = %s WHERE user_id = %s"

    if 'surname' in kwargs.keys():
        value = kwargs['surname']
        sql = "UPDATE testdb.users SET surname = %s WHERE user_id =%s"

    if 'lang' in kwargs.keys():
        value = kwargs['lang']
        sql = "UPDATE testdb.users SET lang = %s WHERE user_id = %s"

    # print(value)
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (value, user_id))
            connection.commit()

    # print('rowcount:', cursor.rowcount)
    # print('affected:', connection.affected_rows())

    if connection.affected_rows() != 0:
        return 'updated'
    else:
        return 'not updated'


# print(update_user_info(19725615, surname='123'))
# print(get_user(197256155))
# print(json.loads(select_all()))
# print(get_columns('users'))
# print(get_user_json(197256155))
# print(update_user_info(197256155, name='1111'))
# print(update_user_info(19725615, name='111111'))
# print(select_all())
# 5, name='dddddd'))
# print(get_user_json(197256155))