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
