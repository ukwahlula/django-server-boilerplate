from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from apps.generic.models import GenericUUIDMixin


class Email(GenericUUIDMixin):
    sender = models.CharField(_("Sender"), max_length=256)
    recipients = models.TextField()

    subject = models.TextField()
    body = models.TextField()

    @property
    def body_html(self):
        return mark_safe(self.body)

    def __str__(self):
        return f"Email from {self.sender} to {self.recipients} sent at {self.created_date} about {self.subject}"

    class Meta:
        verbose_name = _("Email")
        verbose_name_plural = _("Emails")
