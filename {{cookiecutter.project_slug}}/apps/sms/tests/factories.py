import factory

from apps.sms import models


class SmsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Sms
