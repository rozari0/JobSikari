from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Job


@admin.register(Job)
class JobAdmin(ModelAdmin):
    list_display = ("title", "company", "location", "job_type", "is_remote")
    search_fields = ("title", "company", "location")
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
