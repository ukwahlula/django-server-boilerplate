from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.generic.models import GenericUUIDMixin


class Image(GenericUUIDMixin, models.Model):
    creator = models.ForeignKey(
        "users.User", verbose_name=_("Creator"), on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(verbose_name=_("Name"), max_length=255, blank=True, null=True)
    image = models.ImageField(verbose_name=_("Image"), upload_to="storage/images/")

    @property
    def image_url(self):
        if self.image:
            return self.image.url

    def __str__(self):
        return self.name or str(self.pk)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class File(GenericUUIDMixin, models.Model):
    creator = models.ForeignKey(
        "users.User", verbose_name=_("Creator"), on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(verbose_name=_("Name"), max_length=255, blank=True, null=True)
    file = models.FileField(verbose_name=_("File"), upload_to="storage/files/")

    @property
    def file_url(self):
        if self.file:
            return self.file.url

    def __str__(self):
        return self.name or str(self.pk)

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")
