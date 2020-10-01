import factory

from apps.cms import models


class ContentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Content
