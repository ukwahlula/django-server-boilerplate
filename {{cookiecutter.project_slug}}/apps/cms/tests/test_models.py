import pytest

from apps.cms.choices import ContentType
from apps.cms.models import Content
from apps.cms.presets import CONTENT_PRESETS
from apps.generic.management.commands.initcontent import Command


@pytest.mark.django_db
def test_content_model_name(content):
    assert str(content) == content.content_type


@pytest.mark.django_db
def test_content_get_content(content, user):
    for content_type in ContentType.choices():
        content.content_type = content_type[0]
        content.save()
        Content.objects.get_content(content.content_type)


@pytest.mark.django_db
def test_content_presets():
    Command().handle()
    assert Content.objects.all().count() == len(CONTENT_PRESETS.keys())
