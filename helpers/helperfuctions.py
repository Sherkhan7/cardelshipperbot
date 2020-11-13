from DB import get_user


def set_user_data_in_bot_data(user_id, bot_data):
    if user_id not in bot_data.keys() or bot_data[user_id] is False:

        user = get_user(user_id)

        if user:
            user.pop('created_at')
            user.pop('updated_at')

            bot_data[user_id] = user

        else:

            bot_data[user_id] = False


def wrap_tags(*args):
    symbol = ''

    if len(args) > 1:
        symbol = ' '

    return f'<b><i><u>{symbol.join(args)}</u></i></b>'


def format_phone_number(phone_number):
    country_code = phone_number[:4]
    operator_code = phone_number[4:][:2]
    phone_number = phone_number[4:][2:]

    # return value like +998 (99) 855 - 9819

    return f'{country_code} ({operator_code}) {phone_number[:3]} - {phone_number[3:]}'
