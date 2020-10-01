from apps.email.choices import EmailType
from apps.generic.choices import BaseChoices
from apps.sms.choices import SmsType


class ContentType(EmailType, SmsType, BaseChoices):
    pass
