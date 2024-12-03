from django.db.models.signals import post_save, pre_save 
from django.dispatch import receiver
from rest_framework import status
from .models import BookingPending
from bussiness_logic.compute_quote import ComputeQuote
from utils.common_functions import validate_correct_date_time
from utils.api_exceptions import CustomAPIException


# pre save 
@receiver(pre_save, sender = BookingPending)
def pre_save_booking_pending(sender, instance, *args, **kwargs):
    
    if(isinstance(instance, BookingPending)):
        # round distance to the nearest ten 
        rounded_distance = float("%.0f"%round(instance.distance))
        # validate if date is correct 
        if(validate_correct_date_time(instance.booking_date, instance.booking_time)):
            raise CustomAPIException(detail="Invalid Booking date", code=status.HTTP_400_BAD_REQUEST)

        
        # compute the quote
        instance_compute_quote = ComputeQuote(booking_date= instance.booking_date,
                                              distance= rounded_distance,
                                              floors= instance.floors,
                                              helpers= instance.helpers,
                                              user= "customer",
                                              v_type= instance.vehicle_type)
        
        # retrieve pricing
        (base_amount, 
         mid_month_discount, 
         loyal_customer_discount, 
         amount_due_customer) = instance_compute_quote.generate_quote
        
        # set the prices and distance
        instance.distance = rounded_distance
        instance.base_amount = float("%.0f"%round(base_amount))
        instance.mid_month_discount = float("%.0f"%round(mid_month_discount)) 
        instance.loyal_customer_discount = float("%.0f"%round(loyal_customer_discount))  
        instance.amount_due_customer = float("%.0f"%round(amount_due_customer)) 
