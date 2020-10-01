from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.storage.serializers import ImageRetrieveSerializer

from ..models import User
from .mixins import PasswordMixin


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    avatar = ImageRetrieveSerializer()

    class Meta:
        model = User
        fields = (
            "pk",
            "avatar",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birthday",
            "is_phone_verified",
            "is_email_verified",
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "avatar",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birthday",
        )


class ProfilePasswordSerializer(PasswordMixin, serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    repeat_password = serializers.CharField(write_only=True, required=True)

    def validate_current_password(self, value):
        request = self.context.get("request")
        if request and value:
            user = request.user
            if not user.check_password(value):
                raise serializers.ValidationError(_("Password is incorrect."))
        return value

    def save(self, *args, **kwargs):
        self.validated_data.pop("current_password", None)
        return super().save(*args, **kwargs)

    class Meta:
        model = User
        fields = ("current_password", "password", "repeat_password")


class SendVerificationEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("pk", "email")


class SendVerificationSmsSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("pk", "phone")


class VerifyEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    email_verification_code = serializers.CharField(required=True)

    def validate_email_verification_code(self, value):
        if value and not User.objects.filter(is_active=True, email_verification_code=value).exists():
            raise serializers.ValidationError(_("Invalid email verification code."))
        return value

    class Meta:
        model = User
        fields = ("pk", "email", "email_verification_code")


class VerifyPhoneSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    phone_verification_code = serializers.CharField(required=True)

    def validate_phone_verification_code(self, value):
        if value and not User.objects.filter(is_active=True, phone_verification_code=value).exists():
            raise serializers.ValidationError(_("Invalid phone verification code."))
        return value

    class Meta:
        model = User
        fields = ("pk", "phone", "phone_verification_code")
