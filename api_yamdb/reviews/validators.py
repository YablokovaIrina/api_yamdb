import re
import datetime as dt

from django.core.exceptions import ValidationError

from api_yamdb.settings import FORBIDDEN_NAME


def validate_year(value):
    year_now = dt.datetime.now().year
    if value > dt.datetime.now().year:
        raise ValidationError(
            f'Год выпуска {value} не может превышать текущий {year_now}!')
    return value


def validate_username(value):
    if value == FORBIDDEN_NAME:
        raise ValidationError(
            'Имя пользователя {FORBIDDEN_NAME} не разрешено.'
        )
    forbidden_symbols = "".join(set(re.sub(r"[\w.@+-]+", "", value)))
    if forbidden_symbols:
        raise ValidationError(
            f'Имя пользователя содержит недопустимые символы:'
            f'{forbidden_symbols}'
        )
    return value
