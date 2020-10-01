from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import Signal, receiver
from django.utils.crypto import get_random_string

from apps.email.choices import EmailType
from apps.email.generic import Email
from apps.sms.choices import SmsType
from apps.sms.generic import Sms

from .models import User

email_verification = Signal(providing_args=["users"])
phone_verification = Signal(providing_args=["users"])


@receiver(email_verification, sender=User)
def _email_verification(**kwargs):
    users = kwargs.get("users", [])
    for user in users:
        user.is_email_verified = False
        user.email_verification_code = get_random_string(length=6, allowed_chars="0123456789")
    User.objects.bulk_update(users, ("is_email_verified", "email_verification_code"))

    Email(users, EmailType.EMAIL_VERIFICATION_SUBJECT, EmailType.EMAIL_VERIFICATION_BODY).send(
        context_func=lambda user: {"email_verification_code": user.email_verification_code}
    )


@receiver(phone_verification, sender=User)
def _phone_verification(**kwargs):
    users = kwargs.get("users", [])
    for user in users:
        user.is_phone_verified = False
        user.phone_verification_code = get_random_string(length=6, allowed_chars="0123456789")
    User.objects.bulk_update(users, ("is_phone_verified", "phone_verification_code"))

    Sms(users, SmsType.PHONE_VERIFICATION).send(
        context_func=lambda user: {"phone_verification_code": user.phone_verification_code}
    )
