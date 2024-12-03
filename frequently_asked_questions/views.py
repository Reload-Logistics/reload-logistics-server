from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import FrequentlyAskedQuestion
from .serializers import RetrieveFrequentlyAskedQuestionSerializer
from .pagination import Paginator


class RetrieveFrequentlyAskedQuestions(ListAPIView):

    queryset = FrequentlyAskedQuestion.objects.all().order_by("-created_at")
    permission_classes = (AllowAny,)
    serializer_class = RetrieveFrequentlyAskedQuestionSerializer
    pagination_class = Paginator
