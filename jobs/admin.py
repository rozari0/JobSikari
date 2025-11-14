from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Job


@admin.register(Job)
class JobAdmin(ModelAdmin):
    list_display = ("title", "company", "location", "job_type", "is_remote")
    search_fields = ("title", "company", "location")
