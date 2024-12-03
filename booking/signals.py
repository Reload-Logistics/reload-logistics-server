from django.db.models.signals import post_save, pre_save 
from django.dispatch import receiver
# from rest_framework import status
from .models import Booking
from bussiness_logic.compute_quote import ComputeQuote
# from utils.common_functions import validate_correct_date_time
# from utils.api_exceptions import CustomAPIException

# email related 
from utils.email_related_classes import Invoice



@receiver(post_save, sender=Booking)
def post_save_booking(sender, instance = None, created = False, **kwargs):

    if(created):
        # generate_pdf()
        invoice = Invoice(booking=instance)
        invoice.send_invoice_email()



# pre save 
@receiver(pre_save, sender = Booking)
def pre_save_booking(sender, instance, *args, **kwargs):

    if(isinstance(instance, Booking)):
        # round off distance 
        rounded_distance = float("%.0f"%round(instance.distance))

        # # validate_correct_date_time
        # if(validate_correct_date_time(instance.booking_date, instance.booking_time)):
        #     raise CustomAPIException(detail="Invalid Booking date", code=status.HTTP_400_BAD_REQUEST)

        # compute the quote
        instance_compute_quote = ComputeQuote(booking_date= instance.booking_date,
                                              distance= rounded_distance,
                                              floors= instance.floors,
                                              helpers= instance.helpers,
                                              user=instance.customer,
                                              v_type=instance.vehicle_type,
                                              price_adjustment=instance.price_adjustment)
        # retrieve pricing
        (base_amount, 
         mid_month_discount, 
         loyal_customer_discount, 
         amount_due_customer, price_adjustment) = instance_compute_quote.generate_quote
        
        # set the values float("%.0f"%round(customerQuote)) 
        instance.distance = rounded_distance
        instance.base_amount = float("%.0f"%round(base_amount))
        instance.price_adjustment = float("%.0f"%round(price_adjustment))
        instance.mid_month_discount = float("%.0f"%round(mid_month_discount)) 
        instance.loyal_customer_discount = float("%.0f"%round(loyal_customer_discount))  
        instance.amount_due_customer = float("%.0f"%round(amount_due_customer)) 

        # generate_pdf()
        invoice = Invoice(booking=instance)
        booking_cancelation_email_sent = invoice.invoice_cancelation_email()
        
        # set 
        instance.booking_cancelation_email_sent = booking_cancelation_email_sent
