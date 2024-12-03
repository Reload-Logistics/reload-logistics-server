
import googlemaps
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics 

# from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from booking.pagination import Paginator
from decouple import config

from booking.serializer import (CreateBookingSerializer, 
                                RetrieveBookingSerializer, 
                                UpdateBookingSerializer)

from utils.api_exceptions import CustomAPIException
from utils.common_functions import validate_correct_date_time
# models 
from .models import Booking
from bussiness_logic.compute_quote import ComputeQuote

# create Booking 
class CreateBookingAPIVIEW(APIView):

    permission_classes = (IsAuthenticated,)

    # override
    def post(self, request, *args, **kwargs): 

        # payload 
        payload = dict()

        # destructor 
        _ = request.data["customer"] = request.user.id
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
            payload["message"] = "Booking locations must atleast contain a pick up and drop off locations"
            # Respond 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        # verify that the date is correct 
        if(validate_correct_date_time(booking_date, booking_time)):
            # set payload and respond 
            payload["message"] = "Error, booking date time provided is incorrect"
             # Respond 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        # serializer 
        booking_serializer = CreateBookingSerializer(data=request.data, many=False)
        if booking_serializer.is_valid(raise_exception=True):
            booking_serializer.save()
            payload["message"] = "Successfully Created"
            return Response(payload, status=status.HTTP_200_OK)
        return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RetrieveBookingsAPIView(generics.ListAPIView):

    queryset = Booking.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveBookingSerializer
    pagination_class = Paginator
    
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(customer = self.request.user)\
                      .order_by("-created_at")


class RetrieveBookingAPIView(generics.RetrieveAPIView):

    queryset = Booking.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveBookingSerializer
    lookup_field = "pk"

    def get_queryset(self):
        
        # retrieve 
        booking = Booking.objects.filter(pk = self.kwargs.get("pk"))
        if(booking.exists() and (booking.first().customer.pk != self.request.user.pk)):
            raise CustomAPIException(detail="Unauthorized", code=status.HTTP_401_UNAUTHORIZED)
        # return booking
        return booking #super().get_queryset().filter(customer = self.request.user)

    
# UPDATE BOOKING 
class UpdateCustomerBookingAPIView(generics.UpdateAPIView):

    # set queryset
    queryset = Booking.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateBookingSerializer
    lookup_field = "pk"

    # override get_queryset
    def get_queryset(self):

        
        # print(self.request.data)
        booking_date = self.request.data.get("booking_date")
        booking_time = self.request.data.get("booking_time")
        # check date 
        # verify that the date is correct 
        if(booking_date is not None or booking_time is not None):
            if(validate_correct_date_time(booking_date, booking_time)):
                # Respond 
                raise CustomAPIException(detail="Error, booking date and time provided is incorrect", 
                                        code=status.HTTP_400_BAD_REQUEST)

        # extra check 
        booking = Booking.objects.filter(pk = self.kwargs.get("pk"))
        if booking.exists() and self.request.user.pk != booking.first().customer.pk:
            raise CustomAPIException(detail="Unauthorized", code=status.HTTP_401_UNAUTHORIZED)
        
        # resolve 
        retrieved_booking = booking.first()
        if retrieved_booking.booking_canceled or retrieved_booking.booking_completed:
           raise CustomAPIException(detail="Cannot update a canceled of completed booking", 
                                                            code=status.HTTP_400_BAD_REQUEST)
        # otherwise return
        return booking #super().get_queryset().filter(customer = self.request.user)
    

class ComputeQuoteAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
    
        # payload 
        payload = dict()

        # get 
        helpers = request.data.get("helpers")
        floors = request.data.get("floors")
        vehicle_type = request.data.get("vehicle_type")
        distance = request.data.get("distance")
        booking_date = request.data.get("booking_date")

        booking_time = request.data.get("booking_time")
        pickup_dropoff_routes = request.data.get("pickup_dropoff_routes")
        payment_option = request.data.get("payment_option")
        customer_driver_note = request.data.get("customer_driver_note")

        # verify 
        if(booking_time is None or pickup_dropoff_routes is None 
            or payment_option is None or customer_driver_note is None or
                helpers is None or floors is None or 
                vehicle_type is None or distance is None
                        or booking_date is None or distance is None): 
            
            # set payload 
            payload["message"] = "Fields cannot be null"
            # Respond 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        # instance of ComputeQuote
        compute_quote_instance = ComputeQuote(user=request.user, 
                                              distance= float("%.0f"%round(distance)),
                                              booking_date=booking_date,
                                              floors=floors,
                                              helpers=helpers,
                                              v_type=vehicle_type)
        
        (base_amount, 
         mid_month_discount, 
         loyal_customer_discount, 
         amount_due_customer, 
         price_adjustment) = compute_quote_instance.generate_quote
     
        # prices
        request.data["id"] = -999
        request.data["booking_canceled"] = False 
        request.data["booking_completed"] = False 
        request.data["base_amount"] = float("%.0f"%round(base_amount))
        request.data["mid_month_discount"] = float("%.0f"%round( mid_month_discount))
        request.data["loyal_customer_discount"] = float("%.0f"%round(loyal_customer_discount))
        request.data["price_adjustment"] = float("%.0f"%round(price_adjustment))
        request.data["amount_due_customer"] =   float("%.0f"%round(amount_due_customer))
    
        # respond 
        return Response(request.data, status=status.HTTP_200_OK)
    

class ComputeLocationDistance(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        
        #payload 
        payload = dict()
        # retrieve routes 
        pickup_dropoff_routes = request.data.get("pickup_dropoff_routes")

        # verify
        if(pickup_dropoff_routes is None):
            payload["message"] = "Please provide booking pickup and dropoff routes"
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        if(isinstance(pickup_dropoff_routes, list)):

              # // init client      
            client = googlemaps.Client(key = config("GOOGLE_API_KEY", cast=str))
            
            startRoutes, endRoutes = list(), list()

            for index in range(len(pickup_dropoff_routes) - 1):
                
                # routes 
                startRoutes.append((pickup_dropoff_routes[index]["lat"], 
                                    pickup_dropoff_routes[index]["lng"]))
                endRoutes.append((pickup_dropoff_routes[index + 1]["lat"], 
                                  pickup_dropoff_routes[index + 1]["lng"]))
                
                  #// check if theres something in the lists 
            if( len(startRoutes) > 0 and len(endRoutes) > 0): 
                try:
                        #// then this is where we need to do miracles 
                    results = client.distance_matrix(
                                        startRoutes, 
                                        endRoutes,
                                        mode = "driving")
                         #// distance 
                    distance_meters = 0.0
                                    #// forloop
                    for i in range(len(results["rows"])):
                        
                        # retrieve and sum distance 
                        route_distance_meters = results["rows"][i]["elements"][i]["distance"]["value"] #//m 
                        distance_meters += route_distance_meters
                    
                    # respond
                    payload["message"] = "success"
                    payload["distance"] = distance_meters/1000.0 # kms  
                    return Response(payload, status=status.HTTP_200_OK)
            
                except Exception as e:
                                    
                    # set payload 
                    payload["message"] = 'Error {0}'.format(e)
                
                    # respond 
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)
            
                 # ... 
            payload["message"] = "list locations is empty, cant be empty"
            # ... error response 
            return Response(payload, status=status.status.HTTP_400_BAD_REQUEST)

        payload["message"] = "pickup_dropoff_routes should be of type list"
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)












