from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SmsConfig(AppConfig):
    name = "apps.sms"
    verbose_name = _("Sms")
