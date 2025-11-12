from django.db import models
from users.models import Skill


class LearningResource(models.Model):
    class CostChoices(models.TextChoices):
        FREE = "Free", "Free"
        PAID = "Paid", "Paid"

    title = models.CharField(max_length=255)
    platform = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(max_length=1024)
    related_skills = models.ManyToManyField(
        Skill, related_name="learning_resources", blank=True
    )
    cost = models.CharField(
        max_length=10, choices=CostChoices.choices, default=CostChoices.FREE
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.platform})"
