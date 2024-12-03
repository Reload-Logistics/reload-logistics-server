
from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# custom user panel
class UserAdminConfig(UserAdmin):

    readonly_fields = ("email", 
                       "user_first_name", 
                       "user_surname", 
                       "user_contact_number",
                       "date_joined", )
    
    search_fields = ("id", 
                     "email", 
                     "user_first_name", 
                     "user_surname", 
                     "user_contact_number", )
    
    list_filter = ("email", 
                   "user_first_name", 
                   "user_surname", 
                   "user_contact_number",
                   "is_active",)
    
    ordering = ("-date_joined",)

    list_display = ("email",
                    "user_first_name",
                    "user_surname",
                    "user_contact_number",
                    "is_customer",
                    "is_driver",
                    "is_staff",
                    "date_joined",)
    
    fieldsets = ((None, {"fields": (
                            "email",
                            "user_first_name",
                            "user_surname",
                            "user_contact_number",
                            "date_joined",
                            "password",)}),
                ("Permissions", {"fields": (
                            "is_staff",
                            "is_active",
                            "is_verified",
                            "is_superuser",
                            "is_corperate",
                            "is_customer",
                            "is_driver",)}),
                )
# register 
admin.site.register(User, UserAdminConfig)
