from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView

from blogs.models import Blog
from blogs.serializers import BlogSerializer

# Create your views here.


class BlogList(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetail(RetrieveAPIView):
    queryset = Blog.objects.none
    serializer_class = BlogSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Blog.objects.all()
