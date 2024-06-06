from rest_framework import generics

from keedriver import permissions
from.models import FAQ
from .serializers import FAQSerializer
from rest_framework.generics import CreateAPIView
from .serializers import FAQSerializer


class FAQCreateView(CreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsCustomer]