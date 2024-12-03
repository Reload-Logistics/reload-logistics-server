from django.contrib import admin
from .models import ContactUs
# Register your models here.


class ContactUsAdminConfig(admin.ModelAdmin):

    readonly_fields = ("id", 
                       "email", 
                       "name", 
                       "surname", 
                       "subject", 
                       "message", 
                       "responded",
                       "created_at", 
                       "updated_at",)
    
    search_fields = ("email", 
                     "name",
                      "surname", 
                     "id", )
    
    ordering = ("-created_at", )
    
    list_filter =  ("email",
                    "id",
                    "subject",)
    
    list_display = ("id",
                    "email", 
                    "name", 
                    "surname",
                    "subject", 
                    "responded",
                 
                   )
    
        # # # check new
    add_fieldsets = (
        (None, { 
            'classes': ('wide',),
            'fields': ('id',
                    'email', 
                    'name', 
                    'surname',
                    'base_amount', 
                    'subject',
                    'responded',
             
                        ),
        }),
    )


admin.site.register(ContactUs, ContactUsAdminConfig)
