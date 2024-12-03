from django.urls import path
from . import views


# url pattens 
urlpatterns = [
    path("booking/create/", views.CreateBookingPendingAPIVIEW.as_view(), name="create-booking-pending"),
    path("booking/<int:pk>/update/", views.UpdateCustomerBookingAPIView.as_view(), name="update-booking-pending"),
    path("booking/<int:pk>/retrieve/", views.RetrieveBookingPendingAPIView.as_view(), name="retrieve-booking-pending"),
]