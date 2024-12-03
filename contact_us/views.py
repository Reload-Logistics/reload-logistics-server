from rest_framework import generics
from .models import ContactUs
from rest_framework.permissions import AllowAny
from .serializers import CreateContactUsSerializer

class CreateContactUsAPIView(generics.CreateAPIView):

    queryset = ContactUs.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = CreateContactUsSerializer
    lookup_field = "pk"
    