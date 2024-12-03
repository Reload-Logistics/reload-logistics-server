from django.urls import path, include
from django_rest_passwordreset.views import ResetPasswordConfirmViewSet

from . import views

urlpatterns = [
    
    # sigin signout
    path("user/signin/", views.SignInTokenObtainPairView.as_view(), name = "sign-in"),
    path("user/signout/", views.SignOutAPIVIEW.as_view(), name = "sign-out"),
    
    # create user 
    path("user/create/", views.UserCreateAPIVIEW.as_view(), name="create-user"),
    path("user/update/", views.UserUpdateAPIVIEW.as_view(), name = "update-user"),
    path("user/retrieve/", views.UserRetrieveAPIView.as_view(), name = "retrieve-user"),

    # user password reset
    path("user/password/reset/", include('django_rest_passwordreset.urls', namespace='password_reset')),
    path("user/password/reset/confirm/", ResetPasswordConfirmViewSet.as_view({"put": "items"}), name="password-reset-confirm"),
    
]


# user/password/reset/
# requires an email 

