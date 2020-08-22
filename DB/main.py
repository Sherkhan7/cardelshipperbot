import mysql.connector as connector
import json
# import sys
# sys.path.extend(['/home/sherzodbek/PycharmProjects/cardelshipperbot'])
from config.config import DB_CONFIG

conn = connector.connect(
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database']
)

mycursor = conn.cursor()


def insert_user_contact(user_contact):
    phone_number = user_contact.phone_number
    first_name = user_contact.first_name
    last_name = user_contact.last_name
    user_id = user_contact.user_id

    # print(phone_number, first_name, last_name, user_id)
    sql = f"INSERT INTO testdb.users (user_id, first_name, last_name, phone_number, who_is) VALUES (%s, %s, %s, %s, %s)"
    user_contact_values = (user_id, first_name, last_name, phone_number, 2)

    mycursor.execute(sql, user_contact_values)
    conn.commit()

    print(mycursor.rowcount, "record inserted.")

    return mycursor.rowcount


def insert(user_data):
    user_data.pop('code')
    user_data.pop('confirmation')
    user_data_field = tuple(user_data.keys())
    user_data_values = tuple(user_data.values())
    user_data_values_field = list()
    user_data_values_field.extend(['%s'] * len(user_data_values))
    user_data_values_field = tuple(user_data_values_field)

    sql = f"INSERT INTO testdb.users ({','.join(user_data_field)}) VALUES ({','.join(user_data_values_field)})"

    mycursor.execute(sql, user_data_values)
    conn.commit()

    print(mycursor.rowcount, "record inserted.")

    return mycursor.rowcount


def select(user_id):
    mycursor.execute(f'SELECT * FROM testdb.users WHERE user_id = {user_id}')

    columns = mycursor.column_names
    value = mycursor.fetchone()

    if value is None:
        return None

    record = dict()
    for i in range(len(columns)):
        record.update({columns[i]: value[i]})

    record['created_at'] = record['created_at'].strftime('%c')
    record['updated_at'] = record['updated_at'].strftime('%c')

    return json.dumps(record, indent=4)


def select_all():
    mycursor.execute(f'SELECT * FROM testdb.users')

    columns = mycursor.column_names
    records = mycursor.fetchall()

    if records is None:
        return None

    record = dict()
    records_list = list()

    for record_item in records:
        for j in range(len(columns)):
            record.update({columns[j]: record_item[j]})

        record['updated_at'] = record['updated_at'].strftime('%c')
        record['created_at'] = record['created_at'].strftime('%c')

        records_list.append(record)
        record = {}

    return json.dumps(records_list, indent=4)


def update_user_info(user_id):
    mycursor.execute(f"UPDATE testdb.users SET name = 'She232131' WHERE testdb.users.user_id = {user_id}")
    result = conn.commit()

    return 'updated'
