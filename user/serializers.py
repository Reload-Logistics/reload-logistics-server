from rest_framework_simplejwt.tokens import Token
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ImageField

# sign in 
class SigninTokenPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: User) -> Token:
        # return super().get_token(user)
        token = super().get_token(user)

        # set token 
        token["user_first_name"] = user.user_first_name
        token["user_surname"] = user.user_surname
        token["user_contact_number"] = user.user_contact_number
        token["is_driver"] = user.is_driver
        token["is_customer"] = user.is_customer
        token["is_staff"] = user.is_staff
       
        return token 

# Register Serializer 
class RegisterSerializer(ModelSerializer):

    # create meta class 
    class Meta: 
        model = User
        fields = ("email", 
                  "user_first_name",
                  "user_surname",
                  "user_contact_number",
                  "password",
                  "is_customer",
                  "is_driver",
                  "is_staff",
                  "is_corperate",)
        extra_kwargs = {"password": {"write_only": True}}

    # create password 
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if(password is not None):
            instance.set_password(password)
        instance.save()
        return instance
    
class UserUpdateSerializer(ModelSerializer):

    class Meta: 
        model = User
        fields = ["user_first_name", "user_surname", "user_contact_number",]


class UserPresentationSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["id",
                  "email", 
                  "user_first_name", 
                  "user_surname", 
                  "user_contact_number",
                  "is_driver",
                  "is_customer", 
                  "is_staff",]