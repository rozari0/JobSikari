from django.db import models
from users.models import Skill


class Job(models.Model):
    class JobType(models.TextChoices):
        INTERNSHIP = "Internship", "Internship"
        PART_TIME = "Part-time", "Part-time"
        FULL_TIME = "Full-time", "Full-time"
        FREELANCE = "Freelance", "Freelance"

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    is_remote = models.BooleanField(default=False)
    required_skills = models.ManyToManyField(Skill, related_name="jobs", blank=True)
    recommended_experience = models.CharField(max_length=10, blank=True, null=True)
    job_type = models.CharField(
        max_length=20, choices=JobType.choices, default=JobType.FULL_TIME
    )
    description = models.TextField(blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} @ {self.company}"
