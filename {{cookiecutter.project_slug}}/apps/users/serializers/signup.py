from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import User
from .mixins import PasswordMixin


class SignUpSendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(is_active=True, email=email).exists():
            raise serializers.ValidationError(_("User with the email has already registered."))
        return email


class SignUpVerifyEmailSerializer(serializers.ModelSerializer):
    def validate_email_verification_code(self, value):
        if value and not User.objects.filter(is_active=False, email_verification_code=value).exists():
            raise serializers.ValidationError(_("Invalid email verification code."))
        return value

    class Meta:
        model = User
        fields = ("email_verification_code",)


class SignUpSendSmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone",)


class SignUpVerifyPhoneSerializer(serializers.ModelSerializer):
    def validate_phone_verification_code(self, value):
        if value and not User.objects.filter(is_active=False, phone_verification_code=value).exists():
            raise serializers.ValidationError(_("Invalid phone verification code."))
        return value

    class Meta:
        model = User
        fields = ("phone_verification_code",)


class SignUpPasswordSerializer(PasswordMixin, serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password", "repeat_password")


class SignUpProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "avatar",
            "first_name",
            "last_name",
            "phone",
            "birthday",
        )


class SignUpFinishSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk",)
