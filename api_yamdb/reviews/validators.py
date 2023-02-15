import re
import datetime as dt

from django.core.exceptions import ValidationError

from api_yamdb.settings import FORBIDDEN_NAME, FORBIDDEN_NAME_MESSAGE


def validate_year(value):
    year_now = dt.datetime.now().year
    if value > dt.datetime.now().year:
        raise ValidationError(
            f'Год выпуска {value} не может превышать текущий {year_now}!')
    return value


def validate_username(value):
    if value == FORBIDDEN_NAME:
        raise ValidationError(
            FORBIDDEN_NAME_MESSAGE
        )
    symbols = ''.join(re.findall(r'[^\w.@+-]+', value))
    if symbols not in value:
        raise ValidationError(
            f'Имя пользователя содержит недопустимые символы {symbols}'
        )
    return value
