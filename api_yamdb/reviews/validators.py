import re
import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > dt.datetime.now().year:
        raise ValidationError(
            'Год выпуска превышает текущий!')
    return value


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Имя не может быть - me/Me/I.',
            params={'value': value},
        )
    match = re.match(r'^[\w@.+-]+$', value)
    if match is None or match.group() != value:
        raise ValidationError(
            'Имя пользователя может содержать только буквы, '
            'цифры и символы @ . + - _'
        )
    return value
