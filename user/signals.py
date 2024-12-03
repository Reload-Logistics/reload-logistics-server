# from django.conf import settings as _set
from .models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from utils.constant_variables import website_url

from utils.email_related_classes import UserCustomer

# signals 
@receiver(post_save, sender = User)
def registered_user_signal(sender, instance = None, created = False, **kwargs):

    # if created 
    if created:
        user_customer = UserCustomer(instance, "")
        user_customer.send_welcome_message_email()


# password reset 
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    user_customer = UserCustomer(reset_password_token.user, reset_password_token.key)
    user_customer.send_password_reset_email()
    # template data 
    # template_data = {
    #     "user": reset_password_token.user,
    #     "username": reset_password_token.user.user_first_name,
    #     "email": reset_password_token.user.email,
    #     "password_reset_url": f"{website_url}/password/reset/{reset_password_token.key}",
    # }

    # # render template 
    # send email 