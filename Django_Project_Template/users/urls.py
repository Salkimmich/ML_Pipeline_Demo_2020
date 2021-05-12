from django.urls import path

from .views import home_view, signup_view, dashboard_view, download_view
from django.conf import settings
from django.conf.urls.static import static

app_name = "users"

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='sign-up'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('download/', download_view, name='download'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)