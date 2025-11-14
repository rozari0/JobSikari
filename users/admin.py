from django.contrib import admin

# from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin

from .models import User, UserProfile

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    pass


# @admin.register(Group)
# class GroupAdmin(BaseGroupAdmin, ModelAdmin):
#     pass


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    pass
