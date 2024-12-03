from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authentication import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, SigninTokenPairSerializer, UserUpdateSerializer, UserPresentationSerializer


# ... signin access_token and refesh_token
class SignInTokenObtainPairView(TokenObtainPairView):
     # set permissions
    permission_classes = [AllowAny,]
    serializer_class = SigninTokenPairSerializer

# signout
class SignOutAPIVIEW(APIView):

    # set permissions 
    permission_classes = [IsAuthenticated,]

    # post 
    def post(self, request, *args, **kwargs):
        # set payload 
        payload = dict()

        # try to blacklist
        try:
            tokens = OutstandingToken\
                        .objects\
                        .filter(user_id = request.user.id)
            # destructure
            for token in tokens:
                t, _ = BlacklistedToken\
                        .objects.get_or_create(token = token)
            
            # payload 
            payload["message"] = "Successfully signed out"
            # return 
            return Response(payload, status=status.HTTP_200_OK)
        
        except  Exception as e:
            return Response({"message": str(e)}, status= status.HTTP_400_BAD_REQUEST)

    
# Create User 
class UserCreateAPIVIEW(APIView):

    # set permission classes 
    permission_classes = [AllowAny]

    # create user post 
    def post(self, request, *args, **kwargs):

        # set payload 
        payload = dict()

        # verify 
        email = request.data.get("email")
        user_first_name = request.data.get("user_first_name")
        user_surname = request.data.get("user_surname")
        user_contact_number = request.data.get("user_contact_number")
        password = request.data.get("password")

        # brief check
        if(email is None or 
                user_first_name is None or 
                    user_surname is None or 
                        user_contact_number is None or
                                password is None):
            # set payload 
            payload["message"] = "Fields cannot be null"
            
            # return response 
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        # serializer
        register_serializer = RegisterSerializer(data=request.data)
        if register_serializer.is_valid(raise_exception=True):
            user = register_serializer.save()
            if(user):
                # set payload 
                payload["email"] = user.email
                payload["message"] = "Successfully registered with matols"
                # return 
                return Response(payload, status=status.HTTP_201_CREATED)
            # set internal server error 
            payload["message"] = "Internal server Errors"
            return Response(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# user update 
class UserUpdateAPIVIEW(APIView):

    # set permissions 
    permission_classes = [IsAuthenticated,]

    # update
    def put(self, request, *args, **kwargs):

        # set payload 
        payload = dict()

        # verify 
        if isinstance(request.user, get_user_model()):
            # for security purposes
            user = get_object_or_404(get_user_model(), pk = request.user.id)
            user_serializer = UserUpdateSerializer(user, data=request.data)

            # validate 
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # payload 
        payload["message"] = "Unauthorized"
        return Response(payload, status=status.HTTP_401_UNAUTHORIZED)
    

class UserRetrieveAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):

        user = get_object_or_404(get_user_model(), pk = request.user.pk)
        retrieve_user_serializer = UserPresentationSerializer(user, many= False)
        return Response(retrieve_user_serializer.data, status=status.HTTP_200_OK)


        