from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import get_user_model
from utils.constant_variables import *


class BookingPending(models.Model):

    id = models.AutoField(primary_key=True)
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
    
    # locations
    pickup_dropoff_routes = models.JSONField(null=True, blank=True, default=list)

    # booking booleans 
    booking_completed = models.BooleanField(default=NO, choices=YES_NO_CHOICES, null = False, blank=False)
    booking_canceled = models.BooleanField(default=NO, choices = YES_NO_CHOICES, null = False, blank=False)

    # booking date time 
    booking_date = models.DateField(null = True)
    booking_time = models.TimeField(null = True)

    # model date time  
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # overide the string method 
    def __str__(self):
        return 'BOOKING PENDING INVOICE: {0}'.format(self.id)
      
