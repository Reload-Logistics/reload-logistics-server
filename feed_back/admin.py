from django.contrib import admin
from .models import FeedBack


class ModelAdminConfig(admin.ModelAdmin):
    
    readonly_fields = ("customer",
                       "website_feed_back",
                       "service_feed_back",
                       "website_rating",
                       "service_rating",
                       "updated_at",
                       "created_at",)

# register 
admin.site.register(FeedBack, ModelAdminConfig)
