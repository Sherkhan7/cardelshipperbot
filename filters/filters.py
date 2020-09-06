def full_name_filter(full_name):

    full_name = full_name.strip()
    full_name = full_name.split()

    if len(full_name) == 2:
        if full_name[0].isalpha() and full_name[1].isalpha():
            return full_name
        else:
            return False
    else:
        return False


def special_code_filter(special_code):
    if not special_code.isdigit():
        return None

    return int(special_code)


def phone_number_filter(phone_number):

    phone_number = phone_number.replace(" ", "")

    if phone_number.isdigit():

        if len(phone_number) == 9:
            phone_number = '+998' + phone_number

            return phone_number

        elif len(phone_number) == 13:

            return phone_number
    elif phone_number.startswith('+998') and len(phone_number) == 13 and phone_number[1:].isdigit():
        return phone_number

    return None


# print(phone_number_filter('+998998559819'))
