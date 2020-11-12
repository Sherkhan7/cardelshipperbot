from languages import LANGS
from DB import get_region_and_district
from helpers import wrap_tags
from units import UNITS

(USER_ID, FROM_REGION, FROM_DISTRICT, FROM_LOCATION, TO_REGION, TO_DISTRICT, TO_LOCATION, WEIGHT_UNIT, WEIGHT,
 VOLUME_UNIT, VOLUME, DEFINITION, PHOTO, DATE, TIME, CLIENT_PHONE_NUMBER, CONFIRMATION, EDIT) = \
    ('user_id', 'from_region', 'from_district', 'from_location', 'to_region', 'to_district', 'to_location',
     'weight_unit', 'weight', 'volume_unit', 'volume', 'definition', 'photo', 'date', 'time', 'client_phone_number',
     'confirmation', 'edit')


def get_new_cargo_layout(cargo_data, user, lang=None):

    from_point = get_region_and_district(cargo_data[FROM_REGION], cargo_data[FROM_DISTRICT])
    to_point = get_region_and_district(cargo_data[TO_REGION], cargo_data[TO_DISTRICT])
    definition = cargo_data[DEFINITION]
    date = cargo_data[DATE]
    time = cargo_data[TIME]
    client_phone_number = cargo_data[CLIENT_PHONE_NUMBER]
    client_username = f"@{user['username']}"

    if user['lang'] == LANGS[0]:
        from_text = 'Qayerdan'
        from_district_name = from_point[1]['nameUz']
        from_region_name = from_point[0]['nameUz']
        to_text = 'Qayerga'
        to_district_name = to_point[1]['nameUz']
        to_region_name = to_point[0]['nameUz']
        weight_text = 'Yuk og\'irligi'
        volume_text = 'Yuk hajmi'
        definiton_text = 'Yuk tavsifi'
        date_text = 'Yukni jo\'natish kuni'
        time_text = 'Yukni jo\'natish vaqti'
        time_info = 'Hozir'
        client_text = 'E\'lon beruvchi'
        client_phone_number_text = 'Tel nomer'
        receiver_phone_number_text = 'Yukni qabul qiluvchi raqami'
        status_text = 'Status'
        opened_status = 'e\'lon ochiq'
        closed_status = 'e\'lon yopilgan'
        not_confirmed_status = 'e\'lon tasdiqlanmagan'
        tg_account_text = 'Telegram akkaunt'
        undefined_text = 'Noma\'lum'

        # if user_input_data['time'] == 'now':
        #     time_info = "Hozir"
        #     user_input_data['time'] = datetime.datetime.now().strftime('%H:%M')
        # else:
        #     time_info = user_input_data['time']

    if user['lang'] == LANGS[1]:
        from_text = 'Откуда'
        from_district_name = from_point[1]['nameRu']
        from_region_name = from_point[0]['nameRu']
        to_text = 'Куда'
        to_district_name = to_point[1]['nameRu']
        to_region_name = to_point[0]['nameRu']
        weight_text = 'Вес груза'
        volume_text = 'Объем груза'
        definiton_text = 'Описание груза'
        date_text = 'Дата отправки груза'
        time_text = 'Время отправки груза'
        time_info = 'Сейчас'
        client_text = 'Объявитель'
        client_phone_number_text = 'Тел номер'
        receiver_phone_number_text = 'Тел номер получателя груза'
        status_text = 'Статус'
        opened_status = 'объявление открыто'
        closed_status = 'объявление закрыто'
        not_confirmed_status = 'объявление не подтверждено'
        tg_account_text = 'Telegram аккаунт'
        undefined_text = 'Неизвестно'

        # if user_input_data['time'] == 'now':
        #     time_info = "Сейчас"
        # else:
        #     time_info = user_input_data['time']

    if user['lang'] == LANGS[2] or lang:
        from_text = 'Қайердан'
        from_district_name = from_point[1]['nameCy']
        from_region_name = from_point[0]['nameCy']
        to_text = 'Қайерга'
        to_district_name = to_point[1]['nameCy']
        to_region_name = to_point[0]['nameCy']
        weight_text = 'Юк оғирлиги'
        volume_text = 'Юк ҳажми'
        definiton_text = 'Юк тавсифи'
        date_text = 'Юкни жўнатиш куни'
        time_text = 'Юкни жўнатиш вақти'
        time_info = 'Ҳозир'
        client_text = 'Еълон берувчи'
        client_phone_number_text = 'Тел номер'
        receiver_phone_number_text = 'Юкни қабул қилувчи рақами'
        status_text = 'Статус'
        opened_status = 'еълон очиқ'
        closed_status = 'еълон ёпилган'
        not_confirmed_status = 'еълон тасдиқланмаган'
        tg_account_text = 'Телеграм аккаунт'
        undefined_text = 'Номаълум'

        # if user_input_data['time'] == 'now':
        #     time_info = "Hozir"
        #     user_input_data['time'] = datetime.datetime.now().strftime('%H:%M')
        # else:
        #     time_info = user_input_data['time']

    if cargo_data[WEIGHT]:

        if cargo_data[WEIGHT_UNIT] == 'kg':
            m = 0
        elif cargo_data[WEIGHT_UNIT] == 't':
            m = 1

        weight = f'{cargo_data[WEIGHT]} {UNITS[user["lang"]][m]}'

    else:
        weight = undefined_text

    if cargo_data[VOLUME]:
        volume = f'{cargo_data[VOLUME]} {UNITS[user["lang"]][2]}'

    else:
        volume = undefined_text

    if not cargo_data[DEFINITION]:
        definition = undefined_text

    if not user['username']:
        client_username = undefined_text

    if cargo_data['state'] == 'opened':
        status = opened_status
        emoji = '\U0001F7E2'

    elif cargo_data['state'] == 'closed':
        status = closed_status
        emoji = '\U0001F534'

    else:
        status = not_confirmed_status
        emoji = '\U0001F7E1'

    if cargo_data[TIME] == 'now':
        time = time_info

    caption = f'\U0001F4CD  {from_text}: {wrap_tags(from_district_name, from_region_name)}\n' \
              f'\U0001F3C1  {to_text}: {wrap_tags(to_district_name, to_region_name)}\n\n' \
              f'\U0001F4E6  {weight_text}: {wrap_tags(weight)}\n' \
              f'\U0001F4E6  {volume_text}: {wrap_tags(volume)}\n' \
              f'\U0001F5D2  {definiton_text}: {wrap_tags(definition)}\n' \
              f'\U0001F4C6  {date_text}: {wrap_tags(date)}\n' \
              f'\U0001F553  {time_text}: {wrap_tags(time)}\n\n' \
              f'\U0001F464  {client_text}: {wrap_tags(user["name"], user["surname"])}\n' \
              f"\U0001F4DE  {client_phone_number_text}: {wrap_tags(client_phone_number)}\n" \
              f"\U0001F170  {tg_account_text}: {wrap_tags(client_username)}\n\n" \
              f"{emoji}  {status_text}: {wrap_tags(status)}\n\n" \
              f"\U0001F916  @cardel_elonbot \U000000A9\n" \
              f"\U0001F6E1  Cardel Online \U00002122"

    return caption


def get_user_info_layout(user):
    if user['lang'] == LANGS[0]:
        name = 'Ism'
        surname = 'Familya'
        phone = 'Tel'
        phone_2 = 'Tel 2'

    if user['lang'] == LANGS[1]:
        name = 'Имя'
        surname = 'Фамиля'
        phone = 'Тел номер'
        phone_2 = 'Тел номер 2'

    def format_phone_number(phone_number):

        country_code = phone_number[:4]
        operator_code = phone_number[4:][:2]
        phone_number = phone_number[4:][2:]

        # print(country_code, operator_code, phone_number)

        return f'{country_code} ({operator_code}) {phone_number[:3]} - {phone_number[3:]}'

    layout = f"{name}: {wrap_tags(user['name'])}\n\n" \
             f"{surname}: {wrap_tags(user['surname'])}"
    # f"<b><i>{'-'.ljust(30, '-')}</i></b> \n" \
    # f"<b>\U0000260E {phone}: <i><u>{format_phone_number(user['phone_number'])}</u></i></b>" \
    # f"<b><i>\U0000260E {phone_2}: </i><u>{user['phone_number2']}</u></b> \n"

    return layout


def get_phone_number_layout(lang):
    if lang == LANGS[0]:
        text_1 = 'Telefon raqamini quyidagi shaklda yuboring'
        text_2 = 'Misol'
        text_3 = 'Yoki'

    if lang == LANGS[1]:
        text_1 = 'Отправьте номер телефона в виде ниже'
        text_2 = 'Например'
        text_3 = 'Или'

    return f"{text_1}:\n\n" \
           f"{text_2}: {wrap_tags('99 1234567')}\n{text_3}\n" \
           f"{text_2}: {wrap_tags('+998 99 1234567')}\n"

# client_cargo_data = {'client_id': 5,
#                      'client_phone_number': '+998998559819',
#                      'client_user_id': 197256155,
#                      'created_at': datetime.datetime(2020, 11, 11, 21, 53, 55),
#                      'definition': None,
#                      'from_district': 101,
#                      'from_latitude': None,
#                      'from_longitude': None,
#                      'from_region': 87,
#                      'id': 17,
#                      'message_id': 330,
#                      'photo_height': None,
#                      'photo_id': None,
#                      'photo_size': None,
#                      'photo_width': None,
#                      'shipping_datetime': datetime.datetime(2020, 11, 11, 21, 53),
#                      'state': 'closed',
#                      'to_district': 142,
#                      'to_latitude': None,
#                      'to_longitude': None,
#                      'to_region': 132,
#                      'updated_at': datetime.datetime(2020, 11, 11, 21, 53, 55),
#                      'volume': None,
#                      'volume_unit': None,
#                      'weight': None,
#                      'weight_unit': None}
# user = {'lang': 'uz', 'name': 'Sherzodbek', 'surname': 'Esanov'}
# shipping_datetime = client_cargo_data.pop('shipping_datetime')
# client_cargo_data[DATE] = shipping_datetime.strftime('%d-%m-%Y')
# client_cargo_data[TIME] = shipping_datetime.strftime('%H:%M')
# client_user['username'] = 'esanov98'
#
# layout = get_new_cargo_layout(client_cargo_data, user)
#
# print(layout)
