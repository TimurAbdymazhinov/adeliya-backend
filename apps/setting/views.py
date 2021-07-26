from rest_framework import generics

from .models import AppVersion
from .serializers import AppVersionSerializer


class AppVersionAPIView(generics.RetrieveAPIView):
    """
        API view for app version control
    """
    queryset = AppVersion.objects.all()
    serializer_class = AppVersionSerializer

    def get_object(self):
        return self.get_queryset().first()
