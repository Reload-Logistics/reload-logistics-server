from django.urls import path
from . import views


# url pattens 
urlpatterns = [
    # CRUD 
    path("retrieve/user/", views.RetrieveBookingsAPIView.as_view(), name="retrieve-bookings"),
    path("booking/create/", views.CreateBookingAPIVIEW.as_view(), name = "create-booking"),
    path("booking/<int:pk>/update/", views.UpdateCustomerBookingAPIView.as_view(), name="update-booking"),
    path("booking/<int:pk>/retrieve/", views.RetrieveBookingAPIView.as_view(), name = "retrieve-booking"),
    path("booking/compute/distance/", views.ComputeLocationDistance.as_view(), name="compute-distance"),
    path("booking/compute/quote/", views.ComputeQuoteAPIView.as_view(), name="compute-quote"),
]