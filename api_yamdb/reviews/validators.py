import re
import datetime as dt

from django.core.exceptions import ValidationError

from api_yamdb.settings import FORBIDDEN_NAME, FORBIDDEN_NAME_MESSAGE


def validate_year(value):
    if value > dt.datetime.now().year:
        raise ValidationError(
            f'{value} превышает {dt.datetime.now().year}!')
    return value


def validate_username(value):
    if value == FORBIDDEN_NAME:
        raise ValidationError(
            FORBIDDEN_NAME_MESSAGE,
            params={'value': value},
        )
    match = re.match(r"^[\w@.+-]+$", value)
    if match is None:
        raise ValidationError(
            f"Недопустимые символы в username: {match} "
        )
    return value
