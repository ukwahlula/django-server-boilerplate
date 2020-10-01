import pytest

from apps.storage.tests import factories


@pytest.fixture
def image():
    return factories.ImageFactory()


@pytest.fixture
def file_data():
    return factories.FileFactory()
