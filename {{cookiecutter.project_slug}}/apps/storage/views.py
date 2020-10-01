from rest_framework import generics
from rest_framework.parsers import MultiPartParser

from apps.generic.permissions import IsAuthenticatedAndActive

from .models import File, Image
from .serializers import FileCreateSerializer, FileRetrieveSerializer, ImageCreateSerializer, ImageRetrieveSerializer


class ImageCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = ImageCreateSerializer
    parser_classes = (MultiPartParser,)

    def perform_create(self, serializer):
        user = self.request.user if not self.request.user.is_anonymous else None
        serializer.save(creator=user)


class ImageRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = ImageRetrieveSerializer
    queryset = Image.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(creator=self.request.user)


class FileCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = FileCreateSerializer
    parser_classes = (MultiPartParser,)

    def perform_create(self, serializer):
        user = self.request.user if not self.request.user.is_anonymous else None
        serializer.save(creator=user)


class FileRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedAndActive,)
    serializer_class = FileRetrieveSerializer
    queryset = File.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(creator=self.request.user)
