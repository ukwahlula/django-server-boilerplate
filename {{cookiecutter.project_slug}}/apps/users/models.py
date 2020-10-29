from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import FieldTracker
from phonenumber_field.modelfields import PhoneNumberField

from apps.generic.models import GenericUUIDMixin


class User(GenericUUIDMixin, AbstractUser):
    email = models.EmailField(_("Email"), db_index=True, unique=True)
    is_email_verified = models.BooleanField(_("Is email verified"), default=False)
    email_verification_code = models.CharField(
        _("Email Verification Code"), max_length=255, unique=True, null=True, blank=True, db_index=True
    )

    phone = PhoneNumberField(_("Phone"), db_index=True, unique=True, null=True, blank=True)
    is_phone_verified = models.BooleanField(_("Is phone verified"), default=False)
    phone_verification_code = models.CharField(
        _("Phone Verification Code"), max_length=255, unique=True, null=True, blank=True, db_index=True
    )

    is_2fa_enabled = models.BooleanField(_("Is 2fa enabled"), default=False)

    avatar = models.ForeignKey(
        "storage.Image", verbose_name=_("Avatar"), on_delete=models.SET_NULL, null=True, blank=True
    )
    birthday = models.DateField(verbose_name=_("Birthday"), null=True, blank=True)

    reset_password_code = models.CharField(
        _("Reset Password Code"), max_length=255, unique=True, null=True, blank=True, db_index=True
    )

    fields_tracker = FieldTracker(fields=["email"])

    @property
    def full_name(self):
        return self.get_full_name() or self.email

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
