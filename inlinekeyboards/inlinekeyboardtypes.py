from inlinekeyboards.inlinekeyboardvariables import *

inline_keyboard_types = {
    user_data_keyboard: {
        "uz": {
            1: "Ismni o'zgartirish",
            2: "Familyani o'zgartirish",
            3: "Telefon nomerini o'zgartirish",
        },
        "cy": {
            1: "Исмни ўзгартириш",
            2: "Фамиляни ўзгартириш",
            3: "Телефон номерини ўзгартириш",
        },
        "ru": {
            1: "Изменить имя",
            2: "Изменить фамилию",
            3: "Изменить номер телефона",
        }
    },
    regions_keyboard: {
        "uz": {1: "nameUz", "back_btn_text": "Orqaga"},
        "cy": {1: "nameCy", "back_btn_text": "Орқага"},
        "ru": {1: "nameRu", "back_btn_text": "Назад"},
    },
    dates_keyboard: {
        "uz": ["Hozir", "Bugun"],
        "cy": ["Ҳозир", "Бугун"],
        "ru": ["Сейчас", "Cегодня"]
    },
    hours_keyboard: {
        "uz": {"next_btn_text": "Keyingisi", "back_btn_text": "Orqaga"},
        "cy": {"next_btn_text": "Кейингиси", "back_btn_text": "Орқага"},
        "ru": {"next_btn_text": "Следующий", "back_btn_text": "Назад"}
    },
    confirm_keyboard: {
        "uz": ["Tasdiqlash", "Tahrirlash"],
        "cy": ["Тасдиқлаш", "Таҳрирлаш"],
        "ru": ["Подтвердить", "Редактировать"],
    },
    edit_keyboard: {
        "uz": {
            1: "Manzilni tahrirlash",
            2: "Yuk ma'lumotlarini tahrirlash",
            3: "Kun va vaqtni tahrirlash",
            4: "Tahrirni yakunlash",
        },
        "cy": {
            1: "Манзилни таҳрирлаш",
            2: "Юк маълумотларини таҳрирлаш",
            3: "Кун ва вақтни таҳрирлаш",
            4: "Таҳрирни якунлаш",
        },
        "ru": {
            1: "Редактировать адрес",
            2: "Редактировать информацию о грузе",
            3: "Редактировать дату и время",
            4: "Закончить редактирование",

        },
    },
    edit_address_keyboard: {
        "uz": {
            1: "Qayerdan manzilini tahrirlash",
            2: "Qayerdan geolokatsiyasini tahrirlash",
            3: "Qayerga manzilini tahrirlash",
            4: "Qayerga geolokatsiyasini tahrirlash",
            5: "Ortga",
        },
        "cy": {
            1: "Қаердан манзилини таҳрирлаш",
            2: "Қаердан геолокациясини таҳрирлаш",
            3: "Қаерга манзилини таҳрирлаш",
            4: "Қаерга геолокациясини таҳрирлаш",
            5: "Ортга",
        },
        "ru": {
            1: "Редактировать адрес Откуда",
            2: "Редактировать геолокацию Откуда",
            3: "Редактировать адрес  Куда",
            4: "Редактировать геолокацию  Куда",
            5: "Назад",
        }
    },
    edit_cargo_info_keyboard: {
        "uz": {
            1: "Og'irlikni tahrirlash",
            2: "Hajmni tahrirlash",
            3: "Tavsifni tahrirlash",
            4: "Rasmni tahrirlash",
            5: "Telefon raqamini tahrirlash",
            6: "Ortga",
        },
        "cy": {
            1: "Оғирликни таҳрирлаш",
            2: "Ҳажмни таҳрирлаш",
            3: "Тавсифни таҳрирлаш",
            4: "Расмни таҳрирлаш",
            5: "Телефон рақамини таҳрирлаш",
            6: "Ортга",
        },
        "ru": {
            1: "Изменить вес",
            2: "Изменить объем",
            3: "Изменить описание",
            4: "Изменить фотография",
            5: "Изменить номер телефона",
            6: "Назад"
        }
    },
    paginate_keyboard: {
        "uz": ["E'lonni yopish", "E'lonni qayta ochish", "E'lonni qayta ochildi"],
        "cy": ["Эълонни ёпиш", "Эълонни қайта очиш", "Эълонни қайта очилди"],
        "ru": ["Закрыть объявление", "Повторно открыть объявление", "Объявление было повторно открыто"],

    }
}
