import re

from rest_framework.serializers import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Использовать имя "me" в качестве username запрещено.'
        )
    match = re.match(r'^[\w@.+-]+$', value)
    if match is None or match.group() != value:
        raise ValidationError(
            'Имя пользователя может содержать только буквы, '
            'цифры и символы @ . + - _'
        )
    return value
