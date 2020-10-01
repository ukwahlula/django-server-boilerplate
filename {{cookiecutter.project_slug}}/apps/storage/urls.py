from django.urls import path

from .views import FileCreateView, FileRetrieveView, ImageCreateView, ImageRetrieveView

app_name = "apps.storage"

urlpatterns = [
    path("image/create/", ImageCreateView.as_view(), name="image-create"),
    path("image/retrieve/<uuid:pk>/", ImageRetrieveView.as_view(), name="image-retrieve"),
    path("file/create/", FileCreateView.as_view(), name="file-create"),
    path("file/retrieve/<uuid:pk>/", FileRetrieveView.as_view(), name="file-retrieve"),
]
