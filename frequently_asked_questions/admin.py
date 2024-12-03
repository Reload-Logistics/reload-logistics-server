from django.contrib import admin
from .models import FrequentlyAskedQuestion


class ModelAdminConfig(admin.ModelAdmin):

    readonly_fields = ("created_at", "updated_at",)

admin.site.register(FrequentlyAskedQuestion, ModelAdminConfig)