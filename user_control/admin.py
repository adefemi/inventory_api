from django.contrib import admin
from .models import CustomUser, UserActivities


admin.site.register((CustomUser, UserActivities,))
