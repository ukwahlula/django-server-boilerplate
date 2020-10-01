from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CmsConfig(AppConfig):
    name = "apps.cms"
    verbose_name = _("Cms")
