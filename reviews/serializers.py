from rest_framework import serializers
from .models import Review
from accounts.serializers import MyUserSerializer 


class ReviewSerialzer(serializers.ModelSerializer):
    reviewer = MyUserSerializer(read_only=True,)
    review_to = MyUserSerializer(read_only=True,)


    class Meta:
        model = Review
        fields = '__all__'


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('reviewer',)