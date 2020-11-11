def fullname_filter(fullname):
    fullname = fullname.strip()
    fullname = fullname.split()

    if len(fullname) == 2:

        if fullname[0].isalpha() and fullname[-1].isalpha():

            fullname = fullname

        else:
            fullname = False

    return fullname


def special_code_filter(special_code):
    special_code = special_code.replace(' ', '')

    if special_code.isdigit():
        special_code = int(special_code)

    else:
        special_code = False

    return special_code


def phone_number_filter(phone_number):
    phone_number = phone_number.replace(' ', '')

    if phone_number.isdigit():

        if len(phone_number) == 9:
            phone_number = '+998' + phone_number

        elif len(phone_number) == 12 and phone_number.startswith('998'):
            phone_number = '+' + phone_number

        else:
            phone_number = False

    elif len(phone_number) == 13 and phone_number.startswith('+998') and phone_number[1:].isdigit():

        phone_number = phone_number

    else:
        phone_number = False

    return phone_number

# print(phone_number_filter('+99899333222'))
