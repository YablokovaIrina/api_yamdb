from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from api_yamdb.settings import EMAIL_YAMDB
from reviews.models import User


def send_confirmation_code(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {user.confirmation_code}',
        from_email=EMAIL_YAMDB,
        recipient_list=[user.email],
        fail_silently=False,
    )
    user.save()
