
from django.utils import timezone
from django.db import models
from utils.constant_variables import *

class ContactUs(models.Model):

    # fields 
    id = models.AutoField(primary_key=True)
    email = models.CharField(default = '', max_length = 300, null=True, blank=True)
    name = models.CharField(default = '', max_length = 300, null=True, blank=True)
    surname = models.CharField(default = '', max_length = 300, null=True, blank=True)
    subject = models.CharField(default = '', max_length = 300, null=True, blank=True)
    message = models.CharField(default = '', max_length = 300, null=True, blank=True)
    responded  = models.BooleanField(default=NO, choices=YES_NO_CHOICES, null = False, blank=False)
    respond = models.BooleanField(default=NO, choices=YES_NO_CHOICES, null = False, blank=False)
    message_response = models.TextField(default = '', max_length = 2000, null=True, blank=True)
    # model date time  
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Contact us {self.name} {self.surname} {self.id}"
