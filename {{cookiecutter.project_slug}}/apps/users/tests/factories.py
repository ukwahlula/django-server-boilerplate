import factory
from django.conf import settings

from apps.company.tests.factories import CompanyFactory
from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: "user-{0}@example.com".format(n))
    phone = factory.Sequence(lambda n: "+1234{0}".format(n))
    password = factory.PostGenerationMethodCall("set_password", settings.DEFAULT_PASSWORD)
    company = factory.SubFactory(CompanyFactory)

    class Meta:
        model = User
        django_get_or_create = ("email",)
