from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateFeedBackAPIView.as_view(), name="create-feed-back"),
    path("fetch/", views.FetchFeedBacksAPIView.as_view(), name="fetch-feed-back"),
]