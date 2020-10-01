from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.generic.models import GenericUUIDMixin


class Sms(GenericUUIDMixin):
    phone = models.CharField(_("Phone"), max_length=64)
    sms = models.TextField(_("Sms"))

    def __str__(self):
        return f"Sms {self.phone}: {self.sms}"

    class Meta:
        verbose_name = _("Sms")
        verbose_name_plural = _("Sms")
