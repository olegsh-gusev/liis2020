from django.contrib.auth.admin import UserAdmin

from core.models import User

from django.contrib import admin

# admin.site.register(User, UserAdmin)
admin.site.register(User)
