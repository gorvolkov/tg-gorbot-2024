import re


def check_and_format_rating_input(input_str: str) -> str | None:
    """
    Функция для проверки того, что введенная строка может быть преобразована в число с плавающей точкой (float).
    Учитывается возможность ввода в западно-европейском формате (x.xxx...)
    и формате, принятом на территории стран СНГ (x,xxx...)
    """

    eng_float_notation = r"^([1-9](\.\d+)?|10(\.0+)?)$"
    rus_float_notation = r"^([1-9](\,\d+)?|10(\,0+)?)$"

    if re.match(eng_float_notation, input_str):
        return input_str
    elif re.match(rus_float_notation, input_str):
        return input_str.replace(",", ".")
    else:
        return None
