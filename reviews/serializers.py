from rest_framework import serializers

from accounts.serializers import MyUserSerializer

from .models import Review


class ReviewSerialzer(serializers.ModelSerializer):
    reviewer = MyUserSerializer(
        read_only=True,
    )
    review_to = MyUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = "__all__"


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ("reviewer", "review_to")
