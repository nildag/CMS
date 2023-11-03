from django.contrib import admin

from notify.utils.admin import AbstractNotifyAdmin

from .models import Notification

admin.site.register(Notification, AbstractNotifyAdmin)