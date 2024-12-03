from django.urls import path
from . import views

urlpatterns = [
    path("retrieve/all/", views.RetrieveFrequentlyAskedQuestions.as_view(), name="retrieve-faqs"),
]