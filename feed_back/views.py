from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import CreateFeedBackSerializer, FetchFeedBackSerializer
from user.models import User
from .pagination import Paginator
from .models import FeedBack


class CreateFeedBackAPIView(APIView):

    permission_classes = (AllowAny,)

    # override post method
    def post(self, request, *args, **kwargs):

        # payload 
        payload = dict()
        # get 
        request.data["customer"] = (None if request.user.is_anonymous
                                                     else request.user.pk )
        website_feed_back = request.data.get("website_feed_back")
        service_feed_back = request.data.get("service_feed_back")
        website_rating = request.data.get("website_rating")
        service_rating = request.data.get("service_rating")

        # verify 
        if(website_feed_back is None or 
                service_feed_back is None or
                     website_rating is None or service_rating is None):
            
            payload["message"] = "fields cannot be null"
            #return 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        # otherwise 
        if(website_rating < 1 or service_rating < 1 or 
                        website_rating > 5 or service_rating > 5):
            # set payload 
            payload["message"] = "rating cannot be less than 1 and morethan 5"
            # respond 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        # serializer
        feed_back_serializer = CreateFeedBackSerializer(data=request.data, many=False)
        if(feed_back_serializer.is_valid(raise_exception=True)):
            feed_back_serializer.save()
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        return Response(feed_back_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FetchFeedBacksAPIView(generics.ListAPIView):

    queryset = FeedBack.objects.all()
    serializer_class = FetchFeedBackSerializer
    permission_classes = (AllowAny,)
    pagination_class = Paginator

    # is_visible
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(is_visible = True)\
                      .order_by("-created_at")




            
