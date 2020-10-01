from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]

        request = self.context["request"]
        user = authenticate(request, username=email, password=password)
        if user is None or not user.is_active:
            raise serializers.ValidationError(_("Credentials are invalid."))
        if not user.is_active:
            raise serializers.ValidationError(_("Please finish onboarding process."))
        data["user"] = user
        return data


class SignIn2FASerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True)

    def validate(self, data):
        code = data["code"]

        user = User.objects.filter(phone_verification_code=code).first()
        if user is None or not user.is_active:
            raise serializers.ValidationError(_("Code is invalid."))
        if not user.is_active:
            raise serializers.ValidationError(_("Please finish onboarding process."))
        data["user"] = user
        return data
