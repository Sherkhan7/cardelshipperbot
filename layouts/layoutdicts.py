from globalvariables import *

NEW_CARGO_LAYOUT_DICT = {
    "uz": {
        FROM_TEXT: "Qayerdan",
        TO_TEXT: "Qayerga",
        WEIGHT_TEXT: "Yuk og'irligi",
        VOLUME_TEXT: "Yuk hajmi",
        DEFINITION_TEXT: "Yuk tavsifi",
        DATE_TEXT: "Yukni jo'natish kuni",
        TIME_TEXT: "Yukni jo'natish vaqti",
        TIME: "hozir",
        CLIENT_TEXT: "E'lon beruvchi",
        CLIENT_PHONE_NUMBER_TEXT: "Tel nomer",
        STATUS_TEXT: "Status",
        OPENED_STATUS: "e'lon ochiq",
        CLOSED_STATUS: "e'lon yopilgan",
        NOT_CONFIRMED_STATUS: "e'lon tasdiqlanmagan",
        TG_ACCOUNT_TEXT: "Telegram akkaunt",
        UNDEFINED_TEXT: "noma'lum",
        REGION_NAME: 'nameUz'
    },
    "ru": {
        FROM_TEXT: "Откуда",
        TO_TEXT: "Куда",
        WEIGHT_TEXT: "Вес груза",
        VOLUME_TEXT: "Объем груза",
        DEFINITION_TEXT: "Описание груза",
        DATE_TEXT: "Дата отправки груза",
        TIME_TEXT: "Время отправки груза",
        TIME: "сейчас",
        CLIENT_TEXT: "Объявитель",
        CLIENT_PHONE_NUMBER_TEXT: "Тел номер",
        STATUS_TEXT: "Статус",
        OPENED_STATUS: "объявление открыто",
        CLOSED_STATUS: "объявление закрыто",
        NOT_CONFIRMED_STATUS: "объявление не подтверждено",
        TG_ACCOUNT_TEXT: "Telegram аккаунт",
        UNDEFINED_TEXT: "неизвестно",
        REGION_NAME: 'nameRu'
    },
    "cy": {
        FROM_TEXT: "Қайердан",
        TO_TEXT: "Қайерга",
        WEIGHT_TEXT: "Юк оғирлиги",
        VOLUME_TEXT: "Юк ҳажми",
        DEFINITION_TEXT: "Юк тавсифи",
        DATE_TEXT: "Юкни жўнатиш куни",
        TIME_TEXT: "Юкни жўнатиш вақти",
        TIME: "ҳозир",
        CLIENT_TEXT: "Еълон берувчи",
        CLIENT_PHONE_NUMBER_TEXT: "Тел номер",
        STATUS_TEXT: "Статус",
        OPENED_STATUS: "еълон очиқ",
        CLOSED_STATUS: "еълон ёпилган",
        NOT_CONFIRMED_STATUS: "еълон тасдиқланмаган",
        TG_ACCOUNT_TEXT: "Телеграм аккаунт",
        UNDEFINED_TEXT: "номаълум",
        REGION_NAME: 'nameCy'
    }
}

USER_INFO_LAYOUT_DICT = {
    'uz': {
        CLIENT_NAME: "Ism",
        CLIENT_SURNAME: "Familya",
        CLIENT_PHONE_NUMBER: "Tel"
    },
    'cy': {
        CLIENT_NAME: "Исм",
        CLIENT_SURNAME: "Фамиля",
        CLIENT_PHONE_NUMBER: "Тел"
    },
    'ru': {
        CLIENT_NAME: "Имя",
        CLIENT_SURNAME: "Фамилия",
        CLIENT_PHONE_NUMBER: "Тел"
    }
}

PHONE_NUMBER_LAYOUT_DICT = {
    "uz": {
        1: "Telefon raqamini quyidagi shaklda yuboring",
        2: "Misol",
        3: "yoki",
    },
    "cy": {
        1: "Телефон рақамини қуйидаги шаклда юборинг",
        2: "Мисол",
        3: "ёки",
    },
    "ru": {
        1: "Отправьте номер телефона в виде ниже",
        2: "Папример",
        3: "или",
    }
}
