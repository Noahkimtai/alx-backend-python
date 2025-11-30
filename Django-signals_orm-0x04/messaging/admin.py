from django.contrib import admin
from models import Message, Notification

admin.sit.register(Message)
admin.site.register(Notification)
