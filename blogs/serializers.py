from rest_framework import serializers

from blogs.models import Blog


class BlogListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        exclude = ("content",)


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = "__all__"


class BlogPinsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "slug",
        )
