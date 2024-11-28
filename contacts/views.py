from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .serializers import ContactSerializers


@extend_schema(
    tags=["Contacts"],  # Add your custom tag here
)
class ContactCreateView(CreateAPIView):

    serializer_class = ContactSerializers
    permission_classes = {permissions.AllowAny}
