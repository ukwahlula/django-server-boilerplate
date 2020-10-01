import pytest


@pytest.mark.django_db
def test_image_model_name(image):
    assert str(image) == image.name


@pytest.mark.django_db
def test_file_model_name(file):
    assert str(file) == file.name
