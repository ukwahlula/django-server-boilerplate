from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.generic.models import GenericUUIDMixin

from .choices import ContentType


class ContentManager(models.Manager):
    def get_content(self, content_type, context=None):
        try:
            content = self.get(content_type=content_type).content
            if context:
                return content.format(**context)
            return content
        except Content.DoesNotExist:
            return ""


class Content(GenericUUIDMixin, models.Model):
    content_type = models.CharField(_("Content Type"), max_length=64, choices=ContentType.choices(), unique=True)
    content = models.TextField(_("Content"), default="")

    objects = ContentManager()

    def __str__(self):
        return "{content_type}".format(content_type=self.content_type)

    class Meta:
        verbose_name = _("Content")
        verbose_name_plural = _("Content")
