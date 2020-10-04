from languages import LANGS
from DB import *
from units import UNITS

(USER_ID, FROM_REGION, FROM_DISTRICT, FROM_LOCATION, TO_REGION, TO_DISTRICT, TO_LOCATION, WEIGHT_UNIT, WEIGHT,
 VOLUME_UNIT, VOLUME, DEFINITION, PHOTO, DATE, HOUR, MINUTE, RECEIVER_PHONE_NUMBER, CONFIRMATION, EDIT) = \
    ('user_id', 'from_region', 'from_district', 'from_location', 'to_region', 'to_district', 'to_location',
     'weight_unit', 'weight', 'volume_unit', 'volume', 'definition', 'photo',
     'date', 'hour', 'minute', 'receiver_phone_number', 'confirmation', 'edit')


def get_new_cargo_layout(user_input_data, user):
    from_point = get_region_and_district(user_input_data[FROM_REGION], user_input_data[FROM_DISTRICT])
    to_point = get_region_and_district(user_input_data[TO_REGION], user_input_data[TO_DISTRICT])

    if user_input_data[WEIGHT_UNIT] == 'kg':
        m = 0
    else:
        m = 1

    if user['lang'] == LANGS[0]:
        from_text = "Qayerdan"
        from_district_name = from_point[1]['nameUz']
        from_region_name = from_point[0]['nameUz']
        to_text = "Qayerga"
        to_district_name = to_point[1]['nameUz']
        to_region_name = to_point[0]['nameUz']
        weght_text = "Yuk og'irligi"
        weight_unit_name = UNITS['uz'][m]
        volume_text = "Yuk hajmi"
        volume_unit_name = UNITS['uz'][2]
        definiton_text = "Yuk tavsifi"
        date_text = "Yukni jo'natish kuni"
        time_text = "Yukni jo'natish vaqti"
        sender_text = "E'lon beruvchi"
        sender_phone_number_1_text = "Tel nomer"
        receiver_phone_number_text = "Yukni qabul qiluvchi raqami"

        if not user_input_data[WEIGHT]:
            weight_info = "Noma'lum"
        else:
            weight_info = (user_input_data[WEIGHT], weight_unit_name)

        if not user_input_data[VOLUME]:
            volume_info = "Noma'lum"
        else:
            volume_info = (user_input_data[VOLUME], volume_unit_name)

        if not user_input_data[DEFINITION]:
            definition_info = "Noma'lum"
        else:
            definition_info = user_input_data[DEFINITION]

        if not user_input_data[RECEIVER_PHONE_NUMBER]:
            receiver_phone_number_info = "Noma'lum"
        else:
            receiver_phone_number_info = user_input_data[RECEIVER_PHONE_NUMBER]

        if user_input_data['time'] == 'now':
            time_info = "Hozir"
            user_input_data['time'] = datetime.datetime.now().strftime('%H:%M')
        else:
            time_info = user_input_data['time']

    if user['lang'] == LANGS[1]:
        from_text = 'Откуда'
        from_district_name = from_point[1]['nameRu']
        from_region_name = from_point[0]['nameRu']
        to_text = 'Куда'
        to_district_name = to_point[1]['nameRu']
        to_region_name = to_point[0]['nameRu']
        weght_text = 'Вес груза'
        weight_unit_name = UNITS['ru'][m]
        volume_text = 'Объем груза'
        volume_unit_name = UNITS['ru'][2]
        definiton_text = 'Описание груза'
        date_text = 'Дата отправки груза'
        time_text = 'Время отправки груза'
        sender_text = 'Объявитель'
        sender_phone_number_1_text = 'Тел номер'
        receiver_phone_number_text = 'Тел номер получателя груза'

        if not user_input_data[WEIGHT]:
            weight_info = "Неизвестно"
        else:
            weight_info = (user_input_data[WEIGHT], weight_unit_name)

        if not user_input_data[VOLUME]:
            volume_info = "Неизвестно"
        else:
            volume_info = (user_input_data[VOLUME], volume_unit_name)

        if not user_input_data[DEFINITION]:
            definition_info = "Неизвестно"
        else:
            definition_info = user_input_data[DEFINITION]

        if not user_input_data[RECEIVER_PHONE_NUMBER]:
            receiver_phone_number_info = "Неизвестно"
        else:
            receiver_phone_number_info = user_input_data[RECEIVER_PHONE_NUMBER]

        if user_input_data['time'] == 'now':
            time_info = "Сейчас"
            user_input_data['time'] = datetime.datetime.now().strftime('%H:%M')
        else:
            time_info = user_input_data['time']

    def wrap_tags(*args):
        if isinstance(args[0], tuple):
            symbol = ' '
        else:
            symbol = ''

        return f'<b><i><u>{symbol.join(args[0])}</u></i></b>'

    caption = f"\U0001F4CD  {from_text}: {wrap_tags((from_district_name, from_region_name))}\n" \
              f"\U0001F3C1  {to_text}: {wrap_tags((to_district_name, to_region_name))}\n\n" \
              f"\U0001F4E6  {weght_text}: {wrap_tags(weight_info)}\n" \
              f"\U0001F4E6  {volume_text}: {wrap_tags(volume_info)}\n" \
              f"\U0001F4C5	{date_text}: {wrap_tags(user_input_data[DATE])}\n" \
              f"\U0001F553  {time_text}: {wrap_tags(time_info)}\n" \
              f"\U0001F4DE  {receiver_phone_number_text}: {wrap_tags(receiver_phone_number_info)}\n" \
              f"\U0001F5D2	{definiton_text}: {wrap_tags(definition_info)}\n\n" \
              f"\U0001F464  {sender_text}: {wrap_tags((user['name'], user['surname']))}\n" \
              f"\U0001F4DE  {sender_phone_number_1_text}: {wrap_tags(user['phone_number'])}\n\n" \
              f"\U0001F916  @cardelshipperbot \U000000A9\n" \
              f"\U0001F6E1  Cardel Online \U00002122"

    return caption


def get_user_info_layout(user):
    if user['lang'] == LANGS[0]:
        name = 'Ism'
        surname = 'Familya'
        phone = 'Tel'
        # phone_2 = 'Tel 2'

    if user['lang'] == LANGS[1]:
        name = 'Имя'
        surname = 'Фамиля'
        phone = 'Тел номер'
        # phone_2 = 'Тел номер 2'

    def format_phone_number(phone_number):

        country_code = phone_number[:4]
        operator_code = phone_number[4:][:2]
        phone_number = phone_number[4:][2:]

        # print(country_code, operator_code, phone_number)

        return f'{country_code} ({operator_code}) {phone_number[:3]} - {phone_number[3:]}'

    layout = f"<b>{name}: <i><u>{user['name']}</u></i></b>\n\n" \
             f"<b>{surname}: <i><u>{user['surname']}</u></i></b> \n\n" \
             f"<b><i>{'-'.ljust(30, '-')}</i></b> \n" \
             f"<b>\U0000260E {phone}: <i><u>{format_phone_number(user['phone_number'])}</u></i></b>"
    # f"<b><i>\U0000260E {phone_2}: </i><u>{user['phone_number2']}</u></b> \n"

    return layout


def get_phone_number_layout(lang):
    if lang == LANGS[0]:
        text_1 = "Telefon raqamni quyidagi shaklda yuboring"
        text_2 = "Misol"
        text_3 = "Yoki"
        text_4 = "Misol"

    if lang == LANGS[1]:
        text_1 = 'Отправьте номер телефона в виде ниже'
        text_2 = 'Например'
        text_3 = 'Или'
        text_4 = 'Например'

    return f"{text_1}:\n\n" \
           f"<b>{text_2}: <i><u>99 1234567</u></i></b>\n{text_3}\n" \
           f"<b>{text_4}: <i><u>+998 99 1234567</u></i></b>\n"
