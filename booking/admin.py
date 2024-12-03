from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from .models import Booking
from rest_framework.authentication import get_user_model


# custom user panel
class ModelAdminConfig(admin.ModelAdmin):

    readonly_fields = ("customer",
                       "helpers",
                       "vehicle_type",
                       "floors",
                       "booking_canceled",
                       "booking_date",
                       "booking_time",
                       "base_amount",
                       "amount_due_customer",
                       "mid_month_discount", 
                       "loyal_customer_discount",
                       "customer_driver_note",
                       "payment_option",
                       "distance",
                       "booking_cancelation_email_sent",
                       "created_at",)
    
    search_fields = ("vehicle_type", 
                     "customer",
                     "id", )
    
    ordering = ("-created_at", )
    
    
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget(options={"modes": ["view",], 
                                                        "mode": "view",   
                                                        "search": False,})}}
    list_filter =  ("booking_completed",
                    "booking_canceled",
                    "vehicle_type",)
    
    list_display = ("id",
                    "customer", 
                    "vehicle_type", 
                    "amount_due_customer",
                    "base_amount", 
                    "booking_date",
                    "booking_time",
                    "booking_completed",
                   )
    
        # # # check new
    add_fieldsets = (
        (None, { 
            'classes': ('wide',),
            'fields': ('id',
                    'customer', 
                    'vehicle_type', 
                    'amount_due_customer',
                    'base_amount', 
                    'distance',
                    'booking_date',
                    'booking_time',
                        ),
        }),
    )
    
    
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if(db_field.name == "driver"):
            kwargs["queryset"] = get_user_model().objects.filter(is_driver = True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

    

admin.site.register(Booking, ModelAdminConfig)