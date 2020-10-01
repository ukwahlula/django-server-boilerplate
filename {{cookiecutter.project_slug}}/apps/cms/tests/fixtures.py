import pytest

from apps.cms.tests import factories


@pytest.fixture
def content():
    return factories.ContentFactory()
