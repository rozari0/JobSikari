from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import LearningResource


@admin.register(LearningResource)
class LearningResourceAdmin(ModelAdmin):
    list_display = ("title", "platform", "cost")
    search_fields = ("title", "platform")
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
