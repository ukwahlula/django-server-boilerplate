import factory

from apps.storage import models


class ImageFactory(factory.django.DjangoModelFactory):
    image = factory.django.ImageField(filename="picture.png")
    name = factory.Sequence(lambda n: "Image %03d" % n)

    class Meta:
        model = models.Image


class FileFactory(factory.django.DjangoModelFactory):
    file = factory.django.FileField(filename="file.pdf")
    name = factory.Sequence(lambda n: "File %03d" % n)

    class Meta:
        model = models.File
