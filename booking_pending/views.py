from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import BookingPending
from .serializers import (CreateBookingPendingSerializer, 
                          RetrieveBookingPendingSerializer, 
                          UpdateBookingPendingSerializer)

from utils.api_exceptions import CustomAPIException
from utils.common_functions import validate_correct_date_time

# create Booking 
class CreateBookingPendingAPIVIEW(APIView):

    permission_classes = (IsAuthenticated,)

    # override
    def post(self, request, *args, **kwargs): 

        # payload 
        payload = dict()

        # destructor 
        helpers = request.data.get("helpers")
        floors = request.data.get("floors")
        vehicle_type = request.data.get("vehicle_type")
        payment_option = request.data.get("payment_option")
        customer_driver_note = request.data.get("customer_driver_note")
        
        distance = request.data.get("distance")
        pickup_dropoff_routes = request.data.get("pickup_dropoff_routes")

        booking_date = request.data.get("booking_date")
        booking_time = request.data.get("booking_time")

        # verify 
        if(helpers is None or floors is None or 
                vehicle_type is None or payment_option is None or 
                    customer_driver_note is None or distance is None or 
                        pickup_dropoff_routes is None or booking_date is None or
                            booking_time is None): 
            
            # set payload 
            payload["message"] = "Fields cannot be null"
            # Respond 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        # verify that pickup_dropoff_routes are of type list 
        if not isinstance(pickup_dropoff_routes, list):
            # set payload and respond
            payload["message"] = "Booking locations are not of type list"
             # Respond 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        # verify list length 
        if (len(list(pickup_dropoff_routes)) < 2):
            # set payload and respond 
            payload["message"] = "Booking locations cannot ne less than 2"
             # Respond 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        # verify that the date is correct 
        if(validate_correct_date_time(booking_date, booking_time)):
            # set payload and respond 
            payload["message"] = "Error, booking date time provided is incorrect"
             # Respond 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # serializer 
        booking_serializer = CreateBookingPendingSerializer(data=request.data, many=False)
        if booking_serializer.is_valid(raise_exception=True):
            booking_serializer.save()
            payload["message"] = "Successfully Created"
            return Response(payload, status=status.HTTP_200_OK)
        return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveBookingPendingAPIView(generics.RetrieveAPIView):

    queryset = BookingPending.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveBookingPendingSerializer
    lookup_field = "pk"

# UPDATE BOOKING 
class UpdateCustomerBookingAPIView(generics.UpdateAPIView):

    # set queryset
    queryset = BookingPending.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateBookingPendingSerializer
    lookup_field = "pk"


    