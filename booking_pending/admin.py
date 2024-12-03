from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from .models import BookingPending


# custom user panel
class ModelAdminConfig(admin.ModelAdmin):

    readonly_fields = ("booking_date", 
                       "booking_time",
                       "created_at",
                       "base_amount",
                       "amount_due_customer",
                       "mid_month_discount", 
                       "loyal_customer_discount",
                       "customer_driver_note",
                       "payment_option",
                       "distance",)
    
    search_fields = ("vehicle_type", 
                     "", )
    
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget(options={"modes": ["view",], 
                                                        "mode": "view",   
                                                        "search": False,})}}
    

admin.site.register(BookingPending, ModelAdminConfig)