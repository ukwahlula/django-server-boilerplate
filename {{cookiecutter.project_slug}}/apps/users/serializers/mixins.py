from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class PasswordMixin:
    def validate_password(self, value):
        # TODO
        # if not self.instance.check_password(value):
        #     raise serializers.ValidationError(_("Password is incorrect."))
        return value

    def validate(self, data):
        data = super().validate(data)
        if data["password"] != data["repeat_password"]:
            raise serializers.ValidationError({"repeat_password": [_("Passwords do not match")]})
        return data

    def save(self, *args, **kwargs):
        password = self.validated_data.pop("password", None)
        self.validated_data.pop("repeat_password", None)
        if password:
            self.instance.set_password(password)
        return super().save(*args, **kwargs)
