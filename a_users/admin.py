from django.contrib import admin

from a_rtchat.models import ChatGroup, GroupMessage
from .models import Profile

admin.site.register(Profile)
admin.site.register(ChatGroup)
admin.site.register(GroupMessage)

