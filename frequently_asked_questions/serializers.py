from rest_framework import serializers
from .models import FrequentlyAskedQuestion

# 
class RetrieveFrequentlyAskedQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FrequentlyAskedQuestion
        fields = "__all__"

