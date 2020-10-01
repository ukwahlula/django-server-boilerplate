from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import User
from .mixins import PasswordMixin


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if value and User.objects.filter(email=value, is_active=False).exists():
            raise serializers.ValidationError(
                _("User is not active. Please finish a registration or contact with site administration.")
            )
        return value

    class Meta:
        model = User
        fields = ("email",)


class ResetPasswordVerifySerializer(PasswordMixin, serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password", "repeat_password")
