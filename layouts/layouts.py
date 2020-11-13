from DB import get_region_and_district
from helpers import wrap_tags
from units import UNITS
from layouts.layoutdicts import *


def get_new_cargo_layout(cargo_data, lang):
    from_point = get_region_and_district(cargo_data[FROM_REGION], cargo_data[FROM_DISTRICT])
    from_district_name = from_point[1][NEW_CARGO_LAYOUT_DICT[lang][REGION_NAME]]
    from_region_name = from_point[0][NEW_CARGO_LAYOUT_DICT[lang][REGION_NAME]]

    to_point = get_region_and_district(cargo_data[TO_REGION], cargo_data[TO_DISTRICT])
    to_district_name = to_point[1][NEW_CARGO_LAYOUT_DICT[lang][REGION_NAME]]
    to_region_name = to_point[0][NEW_CARGO_LAYOUT_DICT[lang][REGION_NAME]]

    date = cargo_data[DATE]
    time = cargo_data[TIME]
    client_name = cargo_data[CLIENT_NAME]
    client_surname = cargo_data[CLIENT_SURNAME]
    client_phone_number = cargo_data[CLIENT_PHONE_NUMBER]

    weight, volume, definition, client_username = NEW_CARGO_LAYOUT_DICT[lang][UNDEFINED_TEXT]

    if cargo_data[WEIGHT]:
        weight = f'{cargo_data[WEIGHT]} {UNITS[lang][WEIGHT_UNIT]}'

    if cargo_data[VOLUME]:
        volume = f'{cargo_data[VOLUME]} {UNITS[lang][VOLUME_UNIT]}'

    if cargo_data[DEFINITION]:
        definition = cargo_data[DEFINITION]

    if cargo_data[CLIENT_USERNAME]:
        client_username = f'@{cargo_data[CLIENT_USERNAME]}'

    if cargo_data[STATE] == 'opened':
        status = NEW_CARGO_LAYOUT_DICT[lang][OPENED_STATUS]
        emoji = '\U0001F7E2'

    elif cargo_data[STATE] == 'closed':
        status = NEW_CARGO_LAYOUT_DICT[lang][CLOSED_STATUS]
        emoji = '\U0001F534'

    else:
        status = NEW_CARGO_LAYOUT_DICT[lang][NOT_CONFIRMED_STATUS]
        emoji = '\U0001F7E1'

    if cargo_data[TIME] == 'now':
        time = NEW_CARGO_LAYOUT_DICT[lang][TIME]

    layout = f'\U0001F4CD  {FROM_TEXT}: {wrap_tags(from_district_name, from_region_name)}\n' \
             f'\U0001F3C1  {TO_TEXT}: {wrap_tags(to_district_name, to_region_name)}\n\n' \
             f'\U0001F4E6  {WEIGHT_TEXT}: {wrap_tags(weight)}\n' \
             f'\U0001F4E6  {VOLUME_TEXT}: {wrap_tags(volume)}\n' \
             f'\U0001F5D2  {DEFINITION_TEXT}: {wrap_tags(definition)}\n' \
             f'\U0001F4C6  {DATE_TEXT}: {wrap_tags(date)}\n' \
             f'\U0001F553  {TIME_TEXT}: {wrap_tags(time)}\n\n' \
             f'\U0001F464  {CLIENT_TEXT}: {wrap_tags(client_name, client_surname)}\n' \
             f"\U0001F4DE  {CLIENT_PHONE_NUMBER_TEXT}: {wrap_tags(client_phone_number)}\n" \
             f"\U0001F170  {TG_ACCOUNT_TEXT}: {wrap_tags(client_username)}\n\n" \
             f"{emoji}  {STATUS_TEXT}: {wrap_tags(status)}\n\n" \
             f"\U0001F916  @cardel_elonbot \U000000A9\n" \
             f"\U0001F6E1  cardel online \U00002122"

    return layout


def get_user_info_layout(user):
    layout = f"{USER_INFO_LAYOUT_DICT[user['lang']][CLIENT_NAME]}: {wrap_tags(user['name'])}\n\n" \
             f"{USER_INFO_LAYOUT_DICT[user['lang']][CLIENT_SURNAME]}: {wrap_tags(user['surname'])}"
    # f"<b><i>{'-'.ljust(30, '-')}</i></b> \n" \
    # f"<b>\u0000260e {phone}: <i><u>{format_phone_number(user['phone_number'])}</u></i></b>" \
    # f"<b><i>\u0000260e {phone_2}: </i><u>{user['phone_number2']}</u></b> \n"

    return layout


def get_phone_number_layout(lang):
    return f"{PHONE_NUMBER_LAYOUT_DICT[lang][1]}:\n\n" \
           f"{PHONE_NUMBER_LAYOUT_DICT[lang][2]}: {wrap_tags('99 1234567')}\n" \
           f"{PHONE_NUMBER_LAYOUT_DICT[lang][3]}\n" \
           f"{PHONE_NUMBER_LAYOUT_DICT[lang][2]}: {wrap_tags('+998 99 1234567')}\n"
