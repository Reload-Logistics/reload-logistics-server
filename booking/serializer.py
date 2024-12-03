from rest_framework import serializers
from rest_framework.authentication import get_user_model

from user.serializers import UserPresentationSerializer

# ... 
from .models import Booking


# Create Booking Serializer 
class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("customer",     
                   "helpers",
                   "floors",
                   "vehicle_type",
                   "customer_driver_note",
                   "payment_option",
                   "distance",
                   "booking_canceled",
                   "pickup_dropoff_routes",
                   "booking_date",
                   "booking_time",
                   "base_amount",
                   "amount_due_customer",
                   "mid_month_discount",
                   "loyal_customer_discount",
                   "price_adjustment_note",
                   "price_adjustment",
                  )

        
class RetrieveBookingSerializer(serializers.ModelSerializer):

    # .. customer 
    customer = UserPresentationSerializer()
    driver = UserPresentationSerializer()
 
    # meta
    class Meta:
        model = Booking
        fields = ("id",
                  "customer", 
                  "driver",    
                   "helpers",
                   "floors",
                   "vehicle_type",
                   "customer_driver_note",
                   "payment_option",
                   "distance",
                   "booking_canceled",
                   "booking_completed",
                   "pickup_dropoff_routes",
                   "booking_date",
                   "booking_time",
                   "base_amount",
                   "amount_due_customer",
                   "mid_month_discount",
                   "loyal_customer_discount",
                   "price_adjustment",
                   "price_adjustment_note",
                   "created_at",)
        
class UpdateBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ( "helpers",
                   "floors",
                   "vehicle_type",
                   "customer_driver_note",
                   "payment_option",
                   "distance",
                   "booking_canceled",
                   "pickup_dropoff_routes",
                   "booking_date",
                   "booking_time",
                   "price_adjustment",
                   "price_adjustment_note"
                )
