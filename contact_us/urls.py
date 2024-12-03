from django.urls import path
from . import views


urlpatterns = [
  
    # api urls
    path("create/", views.CreateContactUsAPIView.as_view(), name="create-contact-us"),
    
]
