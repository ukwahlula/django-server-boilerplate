import factory

from apps.email import models


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Email
