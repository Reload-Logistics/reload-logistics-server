from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from .managers import UserManager
from utils.constant_variables import *

# Create Custom User model 
class User(AbstractBaseUser, PermissionsMixin):

    # required  
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('email address'), unique = True)
    
    # customer identity 
    user_first_name = models.CharField(max_length=150, null = True, default="")
    user_surname = models.CharField(max_length=150, null = True, default="")
    user_contact_number = models.CharField(max_length=50, null= True, blank= True, default="")

    # date variables 
    date_joined = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    # boolean fields 
    is_active = models.BooleanField(default=YES, choices = YES_NO_CHOICES)
    is_verified = models.BooleanField(default=YES, choices = YES_NO_CHOICES)
    is_terms_cond_accept = models.BooleanField(default=YES, choices = YES_NO_CHOICES)

    # administrations 
    is_staff = models.BooleanField(default=NO, choices = YES_NO_CHOICES)
    is_corperate = models.BooleanField(default=NO, choices = YES_NO_CHOICES)
    is_customer = models.BooleanField(default=NO, choices = YES_NO_CHOICES)
    is_driver = models.BooleanField(default=NO, choices = YES_NO_CHOICES)


    # set default fields 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["user_first_name", "user_surname", "user_contact_number"]

    # set objects 
    objects = UserManager()

    # set string representations 
    def __str__(self):
        return f"{self.user_first_name} {self.user_surname}, Primary key {self.pk}"
    
