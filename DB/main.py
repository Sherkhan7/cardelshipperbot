import pymysql.cursors
from contextlib import closing
import json
import datetime
from config.config import DB_CONFIG
from pprint import pprint


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
users_table_name = 'cardel_elonbot_users'
regions_table_name = 'regions_v2'
cargoes_table_name = 'cardel_elonbot_cargoes'


def insert_user(user_data):
    user_data_field = tuple(user_data.keys())
    user_data_values = tuple(user_data.values())
    user_data_values_field = list()
    user_data_values_field.extend(['%s'] * len(user_data_values))
    user_data_values_field = tuple(user_data_values_field)

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO testdb.{users_table_name} ({','.join(user_data_field)}) " \
                  f"VALUES ({','.join(user_data_values_field)})"
            cursor.execute(sql, user_data_values)
            connection.commit()

    # print(cursor.rowcount, "record inserted.")

    return cursor.rowcount


def get_user(id):
    if id:
        with closing(get_connection()) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM testdb.{users_table_name} WHERE tg_id = %s OR id = %s", (id, id))
                record = cursor.fetchone()

    if record is None:
        return False

    return record


def get_user_json(user_id):
    user = get_user(user_id)
    user['created_at'] = user['created_at'].strftime('%c')
    user['updated_at'] = user['updated_at'].strftime('%c')

    return json.dumps(user, indent=4)


def select_all_users():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM testdb.{users_table_name}')
        records = cursor.fetchall()

    # print(cursor.rowcount)
    return records


def update_user_info(id, **kwargs):
    if 'name' in kwargs.keys():
        value = kwargs['name']
        sql = f"UPDATE testdb.{users_table_name} SET name = %s WHERE tg_id = %s OR id = %s"

    if 'surname' in kwargs.keys():
        value = kwargs['surname']
        sql = f"UPDATE testdb.{users_table_name} SET surname = %s WHERE tg_id =%s OR id = %s"

    if 'lang' in kwargs.keys():
        value = kwargs['lang']
        sql = f"UPDATE testdb.{users_table_name} SET lang = %s WHERE tg_id = %s OR id = %s"

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (value, id, id))
            connection.commit()

    # print('rowcount:', cursor.rowcount)
    # print('affected:', connection.affected_rows())

    return_value = 'not updated'

    if connection.affected_rows() != 0:
        return_value = 'updated'

    return return_value


def select_all_regions():
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM testdb.{regions_table_name} WHERE parent_id = 0")
            regions = cursor.fetchall()

    return regions


def select_all_districts(region_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM testdb.{regions_table_name} WHERE parent_id = %s", region_id)
            districts = cursor.fetchall()

    return districts


def get_region_and_district(region_id, district_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM testdb.{regions_table_name} WHERE id = %s or id = %s",
                           (region_id, district_id))
            regions = cursor.fetchall()

    return regions


def insert_cargo(cargo_data):
    # with open('jsons/cargo.json', 'w') as cargo:
    #     cargo.write(json.dumps(cargo_data, indent=4))
    if cargo_data['message_id']:
        cargo_data.pop('message_id')

    date = cargo_data.pop('date')
    time = cargo_data.pop('time')

    if time == 'now':
        time = datetime.datetime.now().strftime('%H:%M')
    shipping_datetime = datetime.datetime.strptime(date + ' ' + time, '%d-%m-%Y %H:%M')
    cargo_data.update({'shipping_datetime': shipping_datetime})

    from_location = cargo_data.pop('from_location')
    to_location = cargo_data.pop('to_location')
    cargo_photo = cargo_data.pop('photo')

    if from_location:
        cargo_data.update({'from_longitude': from_location['longitude']})
        cargo_data.update({'from_latitude': from_location['latitude']})

    if to_location:
        cargo_data.update({'to_longitude': to_location['longitude']})
        cargo_data.update({'to_latitude': to_location['latitude']})

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

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO testdb.{cargoes_table_name} ({','.join(cargo_data_field)})" \
                  f"VALUES ({','.join(cargo_data_values_field)})"

            try:
                cursor.execute(sql, cargo_data_values)
                connection.commit()
            except pymysql.Error as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
                return False

            # cursor.execute("SELECT * FROM testdb.cargoes WHERE id = %s", cursor.lastrowid)
            # cargo = cursor.fetchone()

    print(cursor.rowcount)

    return cursor.lastrowid


def get_cargo_by_id(cargo_id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM testdb.{cargoes_table_name} WHERE id = %s", cargo_id)
            cargo = cursor.fetchone()

    return cargo


def get_user_cargoes(id):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            sql = f"SELECT * FROM testdb.{cargoes_table_name} WHERE user_id = %s or user_tg_id = %s ORDER BY id DESC"
            cursor.execute(sql, (id, id))
            cargoes = cursor.fetchall()

    return cargoes


def update_cargo_status(cargo_id, status):
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE testdb.{cargoes_table_name} SET state = %s WHERE id = %s", (status, cargo_id))
            connection.commit()

    value = 'not updated'

    if connection.affected_rows() != 0:
        value = 'updated'

    return value


# pprint(get_user_cargoes(2))
