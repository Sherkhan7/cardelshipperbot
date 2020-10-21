from DB import get_user


def set_user_data_in_bot_data(user_id, bot_data):
    if user_id not in bot_data.keys() or bot_data[user_id] is False:

        user = get_user(user_id)

        if user:
            bot_data[user_id] = {'id': user['id'], 'user_id': user['user_id'], 'name': user['name'],
                                 'surname': user['surname'], 'first_name': user['first_name'],
                                 'phone_number': user['phone_number'], 'lang': user['lang'],
                                 'phone_number2': user['phone_number2']}
        else:
            bot_data[user_id] = False
