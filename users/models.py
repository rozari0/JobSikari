from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django_lifecycle import (
    AFTER_CREATE,
    BEFORE_CREATE,
    LifecycleModel,
    LifecycleModelMixin,
    hook,
)

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField("email address", unique=True)

    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Skill(LifecycleModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    @hook(BEFORE_CREATE)
    def set_slug(self):
        self.slug = slugify(self.name)

    def __str__(self):
        return self.name


class Careers(LifecycleModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class UserProfile(LifecycleModel):
    class EducationLevel(models.TextChoices):
        HIGH_SCHOOL = "HS", "High School"
        COLLEGE = "CL", "College"
        BACHELORS = "BA", "Bachelors"
        MASTERS = "MA", "Masters"
        DOCTORATE = "PhD", "Doctorate"

    class ExperienceLevel(models.TextChoices):
        INTERN = "IN", "Intern"
        JUNIOR = "JR", "Junior"
        MID = "MD", "Mid"
        SENIOR = "SR", "Senior"
        LEAD = "LD", "Lead"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullname = models.CharField(max_length=255)
    education = models.CharField(
        max_length=3, choices=EducationLevel.choices, blank=True, null=True
    )
    bio = models.TextField(blank=True, null=True)
    experience = models.CharField(
        max_length=2, choices=ExperienceLevel.choices, blank=True, null=True
    )
    skills = models.ManyToManyField(Skill, related_name="user_profiles", blank=True)
    preferred_careers = models.ManyToManyField(
        Careers, related_name="interested_users", blank=True
    )
