
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# set site 
admin.site.site_title = "Reload"
admin.site.site_header = "Reload Logistics Services (Pty) Ltd"
admin.site.site_url = "https://reload.co.za"


urlpatterns = [
    path('admin/', admin.site.urls),
    # api urls
    path("users/api/", include("user.urls")),
    path("bookings/api/", include("booking.urls")),
    path("bookings/pending/api/", include("booking_pending.urls")),
    path("feed/back/api/", include("feed_back.urls")),
    path("frequently/asked/questions/api/", include("frequently_asked_questions.urls")),
    path("contact/us/api/", include("contact_us.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
