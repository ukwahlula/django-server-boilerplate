from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmailConfig(AppConfig):
    name = "apps.email"
    verbose_name = _("Email")
