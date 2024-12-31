from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from blogs.models import Blog
from blogs.serializers import BlogListSerializer, BlogPinsSerializer, BlogSerializer

# Create your views here.


@extend_schema(
    tags=["Blog"],  # Add your custom tag here
)
class BlogList(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]


@extend_schema(
    tags=["Blog"],  # Add your custom tag here
)
class BlogDetail(RetrieveAPIView):
    queryset = Blog.objects.none
    serializer_class = BlogSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Blog.objects.all()


@extend_schema(
    tags=["Blog"],  # Add your custom tag here
)
class BlogPinsList(ListAPIView):
    queryset = Blog.objects.filter(pin=True)
    serializer_class = BlogPinsSerializer
    permission_classes = [AllowAny]
