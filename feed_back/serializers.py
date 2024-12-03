from rest_framework import serializers
from .models import FeedBack

class CreateFeedBackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedBack
        fields = (
                "customer",
                "website_feed_back",
                "service_feed_back",
                "website_rating",
                "service_rating",
            )

class FetchFeedBackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedBack
        fields = (
                "customer",
                "service_feed_back",
                "service_rating",
            )