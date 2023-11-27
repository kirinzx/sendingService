from django.contrib import admin
from .models import Sending, ClientFilter, Message

admin.site.register(Sending)
admin.site.register(ClientFilter)
admin.site.register(Message)