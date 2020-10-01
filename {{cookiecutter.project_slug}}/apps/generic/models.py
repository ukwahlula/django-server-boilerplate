import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class GenericUUIDMixin(models.Model):
    id = models.UUIDField(db_column="uuid", primary_key=True, default=uuid.uuid4, editable=False)

    created_date = models.DateTimeField(_("Created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("Updated date"), auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_date"]
