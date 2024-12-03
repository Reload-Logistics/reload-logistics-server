from rest_framework import serializers
from .models import BookingPending


# create Pending booking serializer 
class CreateBookingPendingSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = BookingPending
        fields = ("helpers",
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
                   "loyal_customer_discount",)
        
class RetrieveBookingPendingSerializer(serializers.ModelSerializer):

    class Meta: 
        model = BookingPending
        fields = ( "id",
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
                   "loyal_customer_discount",)
        

# update pending booking 
class UpdateBookingPendingSerializer(serializers.ModelSerializer):

    class Meta: 
        model = BookingPending
        fields = ( "helpers",
                   "floors",
                   "vehicle_type",
                   "customer_driver_note",
                   "payment_option",
                   "distance",
                   "booking_canceled",
                   "pickup_dropoff_routes",
                   "booking_date",
                   "booking_time",)