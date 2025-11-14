from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import LearningResource


@admin.register(LearningResource)
class LearningResourceAdmin(ModelAdmin):
    list_display = ("title", "platform", "cost")
    search_fields = ("title", "platform")
