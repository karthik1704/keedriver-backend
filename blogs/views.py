from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from blogs.models import Blog
from blogs.serializers import BlogListSerializer, BlogPinsSerializer, BlogSerializer

# Create your views here.


class BlogList(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]


class BlogDetail(RetrieveAPIView):
    queryset = Blog.objects.none
    serializer_class = BlogSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Blog.objects.all()


class BlogPinsList(ListAPIView):
    queryset = Blog.objects.filter(pin=True)
    serializer_class = BlogPinsSerializer
    permission_classes = [AllowAny]