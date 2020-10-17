# import sys
# sys.path.extend(['/home/sherzodbek/PycharmProjects/cardelshipperbot'])
import pymysql.cursors
from contextlib import closing
import json
import datetime
import pprint
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


def get_user(user_id=None, phone_number=None):
    if user_id:
        with closing(get_connection()) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM testdb.users WHERE user_id = %s", user_id)
                record = cursor.fetchone()

    if phone_number:
        with closing(get_connection()) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM testdb.users WHERE phone_number = %s or phone_number2 = %s",
                               (phone_number, phone_number))
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
    user['created_at'] = user['created_at'].strftime('%c')
    user['updated_at'] = user['updated_at'].strftime('%c')

    return json.dumps(user, indent=4)


def check_user(user_id):
    user = get_user(user_id)

    if user:
        return True

    return False


def select_all():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM testdb.users')
        records = cursor.fetchall()

    # print(cursor.rowcount)

    """ returns list of dicts"""
    return records


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

    if 'phone_number' in kwargs.keys():
        value = kwargs['phone_number']
        sql = "UPDATE testdb.users SET phone_number = %s WHERE user_id = %s"

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


def select_all_regions():
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM testdb.regions WHERE parent_id = %s", 0)
            regions = cursor.fetchall()

    return regions


def select_all_districts(region_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM testdb.regions WHERE parent_id = %s", region_id)
            districts = cursor.fetchall()

    return districts


def get_region_and_district(region_id, district_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM testdb.regions WHERE id = %s or id = %s", (region_id, district_id))
            regions = cursor.fetchall()

    return regions


def insert_cargo(cargo_data):
    # with open('jsons/cargo.json', 'w') as cargo:
    #     cargo.write(json.dumps(cargo_data, indent=4))
    if cargo_data.get('message_id'):
        cargo_data.pop('message_id')

    date = cargo_data.pop('date')
    time = cargo_data.pop('time')

    if time == 'now':
        time = datetime.datetime.now().strftime('%H:%M')

    shipping_datetime = datetime.datetime.strptime(date + ' ' + time, '%d-%m-%Y %H:%M')
    cargo_data.update({'shipping_datetime': shipping_datetime})

    from_location = cargo_data.pop('from_location')
    to_location = cargo_data.pop('to_location')

    if from_location:
        cargo_data.update({'from_longitude': from_location['longitude']})
        cargo_data.update({'from_latitude': from_location['latitude']})

    if to_location:
        cargo_data.update({'to_longitude': to_location['longitude']})
        cargo_data.update({'to_latitude': to_location['latitude']})

    cargo_photo = cargo_data.pop('photo')

    if cargo_photo:
        cargo_data.update({'photo_id': cargo_photo['file_id']})
        cargo_data.update({'photo_width': cargo_photo['width']})
        cargo_data.update({'photo_height': cargo_photo['height']})
        cargo_data.update({'photo_size': cargo_photo['file_size']})

    # pprint.pprint(cargo_data)
    # exit()

    cargo_data_field = tuple(cargo_data.keys())
    cargo_data_values = tuple(cargo_data.values())
    cargo_data_values_field = list()

    cargo_data_values_field.extend(['%s'] * len(cargo_data_values))
    cargo_data_values_field = tuple(cargo_data_values_field)

    # print(cargo_data)
    # print(cargo_data_values)
    # print(cargo_data_field)
    # exit()

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO testdb.cargoes ({','.join(cargo_data_field)})" \
                  f"VALUES ({','.join(cargo_data_values_field)})"

            cursor.execute(sql, cargo_data_values)
            connection.commit()
            #
            # cursor.execute("SELECT * FROM testdb.cargoes WHERE id = %s", cursor.lastrowid)
            # cargo = cursor.fetchone()

    print(cursor.rowcount)

    return cursor.lastrowid


def update_cargo_status(cargo_id, status):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE testdb.cargoes SET state = %s WHERE id = %s", (status, cargo_id))
            connection.commit()

    if connection.affected_rows() != 0:
        return 'updated'
    else:
        return 'not updated'

# print(update_cargo_status(1, 'r'))
# print(get_cargo(25))
# f = open('../jsons/cargo.json', 'r')

# print(type(f.read()))
# cargo_data = json.loads(f.read())
# print(cargo_data)
# receiver = get_user(phone_number='+998998559815')
# print(receiver)
# print(insert_cargo(cargo_data))
# print(get_user('653634001'))
