from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import get_user_model
from utils.constant_variables import *

# create booking model 
class Booking(models.Model):

    # fields 
    id = models.AutoField(primary_key=True)

    # personel identity
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                                    related_name=_("customer_identity"), null=True) 
    driver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                                    related_name=_("driver_identity"), null=True, blank=True)
    
    # booking identity 
    helpers = models.IntegerField(default = 1, choices=HELPERCHOICES, null = True, blank = True)
    floors = models.IntegerField(default = 0, choices=FLOORSCHOICES, null = True, blank = True)
    payment_option = models.CharField(default = 'CASH', choices=PAYMENTOPTIONS, max_length = 50, null=True, blank=True)
    customer_driver_note = models.TextField(default= 'None applicable', max_length = 1000, null = True, blank = True)
    vehicle_type = models.FloatField(default = 1.0, choices=VEHICLESIZECHOICES, null = True, blank = True)

    # financial information 
    base_amount = models.FloatField(default = 0.0, null = True, blank = True)
    amount_due_customer = models.FloatField(default = 0.0, null = True, blank = True)
    mid_month_discount = models.FloatField(default = 0.0, null = True, blank = True)
    distance = models.FloatField(default = 0.0, null = True, blank = True)
    loyal_customer_discount = models.FloatField(default = 0.0, null = True, blank = True)
    price_adjustment = models.FloatField(default = 0.0, null = True, blank = True)
    price_adjustment_note = models.CharField(default = '', max_length = 1500, null=True, blank=True)
    
    # locations
    pickup_dropoff_routes = models.JSONField(null=True, blank=True, default=list)

    # booking booleans 
    booking_completed = models.BooleanField(default=NO, choices=YES_NO_CHOICES, null = False, blank=False)
    booking_canceled = models.BooleanField(default=NO, choices = YES_NO_CHOICES, null = False, blank=False)
    booking_cancelation_email_sent = models.BooleanField(default=NO, choices = YES_NO_CHOICES, null = False, blank=False)

    # booking date time 
    booking_date = models.DateField(null = True)
    booking_time = models.TimeField(null = True)

    # model date time  
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # overide the string method 
    def __str__(self):
        return f"BOOKING INVOICE: {self.id}"
      
