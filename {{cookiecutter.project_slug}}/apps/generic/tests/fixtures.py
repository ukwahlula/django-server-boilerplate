import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.views import APIView

from apps.generic.permissions import IsAuthenticatedAndActive


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def is_authenticated_and_active_class_view():
    class IsAuthenticatedAndActiveView(APIView):
        permission_classes = (IsAuthenticatedAndActive,)

        def get(self, request, *args, **kwargs):
            return Response({})

    return IsAuthenticatedAndActiveView
