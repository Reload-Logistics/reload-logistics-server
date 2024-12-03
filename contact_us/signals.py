from django.db.models.signals import post_save, pre_save 
from django.dispatch import receiver
# email related 
from utils.email_related_classes import UserContactUs

# .. model 
from .models import ContactUs



@receiver(post_save, sender=ContactUs)
def contact_us_created_signal(sender, instance = None, created = False, **kwargs):
    
    # if created
    if(created):
        contact_us = UserContactUs(instance=instance)
        contact_us.send_thank_you_email()


@receiver(pre_save, sender = ContactUs)
def contact_us_presave_signal(sender, instance, *args, **kwargs):

    if(isinstance(instance, ContactUs)):
        contact_us = UserContactUs(instance=instance)
        reponded = contact_us.send_response_email()
        instance.responded = reponded

