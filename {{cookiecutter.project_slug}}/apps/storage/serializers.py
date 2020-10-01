from rest_framework import serializers
from rest_framework.fields import FileField, ImageField

from .models import File, Image


class ImageCreateSerializer(serializers.ModelSerializer):
    image = ImageField(required=True)

    def create(self, validated_data):
        image = validated_data.get("image")
        validated_data["name"] = image._name
        return super().create(validated_data)

    class Meta:
        model = Image
        fields = ("pk", "image")


class ImageRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("pk", "image_url")


class FileCreateSerializer(serializers.ModelSerializer):
    file = FileField(required=True)

    def create(self, validated_data):
        file = validated_data.get("file")
        validated_data["name"] = file._name
        return super().create(validated_data)

    class Meta:
        model = File
        fields = ("pk", "file")


class FileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ("pk", "file_url")
