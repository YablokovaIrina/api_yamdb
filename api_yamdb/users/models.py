from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'


class User(AbstractUser):
    USER_ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )

    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Имя пользователя',
        validators=(validate_username,),
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Адрес электронной почты',
    )
    role = models.CharField(
        max_length=15,
        choices=USER_ROLE_CHOICES,
        default=USER,
        verbose_name='Роль пользователя',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография пользователя',
    )
    confirmation_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Код подтверждения',
    )

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
