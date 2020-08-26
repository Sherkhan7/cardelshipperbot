def full_name_filter(full_name, user_input_data):
    full_name = user_input_data.pop('full_name')
    full_name = full_name.strip()
    full_name = full_name.split()

    if len(full_name) == 2:
        if full_name[0].isalpha() and full_name[1].isalpha():
            return full_name
        else:
            return None
    else:
        return None


def special_code_filter(special_code):
    if not special_code.isdigit():
        return None

    return int(special_code)
