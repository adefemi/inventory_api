
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_control.urls')),
    path('app/', include('app_control.urls')),
]
