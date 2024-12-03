from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import get_user_model
from utils.constant_variables import *

class FeedBack(models.Model):

    # id 
    id = models.AutoField(primary_key=True)

    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                                    related_name=_("customer"), null=True, blank=True) 

    website_feed_back = models.CharField(default = "", max_length = 1500, null=True, blank=True)
    service_feed_back = models.CharField(default = "", max_length = 1500, null=True, blank=True)

    website_rating = models.IntegerField(default = 1, choices= RATING, null = True, blank = True)
    service_rating = models.IntegerField(default = 1, choices= RATING, null = True, blank = True)

    is_visible = models.BooleanField(default=YES, choices=YES_NO_CHOICES, null = False, blank=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Service and Website Rating {self.id}"
