"""
Tests for matching logic and dashboard API endpoints.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from jobs.models import Job
from resources.models import LearningResource
from users.models import Skill, UserProfile
from users.matching import (
    calculate_skill_overlap,
    match_jobs_for_user,
    match_resources_for_user,
)

User = get_user_model()


class SkillOverlapTests(TestCase):
    """Tests for skill overlap calculation."""

    def test_perfect_overlap(self):
        """User has all required skills."""
        user_skills = {"python", "django", "sql"}
        required_skills = {"python", "django", "sql"}
        overlap = calculate_skill_overlap(user_skills, required_skills)
        self.assertEqual(overlap, 1.0)

    def test_partial_overlap(self):
        """User has some of the required skills."""
        user_skills = {"python", "django"}
        required_skills = {"python", "django", "sql", "aws"}
        overlap = calculate_skill_overlap(user_skills, required_skills)
        self.assertEqual(overlap, 0.5)  # 2 out of 4

    def test_no_overlap(self):
        """User has none of the required skills."""
        user_skills = {"javascript", "react"}
        required_skills = {"python", "django"}
        overlap = calculate_skill_overlap(user_skills, required_skills)
        self.assertEqual(overlap, 0.0)

    def test_empty_required_skills(self):
        """No skills required gives baseline match."""
        user_skills = {"python", "django"}
        required_skills = set()
        overlap = calculate_skill_overlap(user_skills, required_skills)
        self.assertEqual(overlap, 0.5)

    def test_empty_user_skills(self):
        """User with no skills gets zero match."""
        user_skills = set()
        required_skills = {"python", "django"}
        overlap = calculate_skill_overlap(user_skills, required_skills)
        self.assertEqual(overlap, 0.0)


class JobMatchingTests(TestCase):
    """Tests for job matching logic."""

    def setUp(self):
        """Create test user, skills, and jobs."""
        # Create skills
        self.python = Skill.objects.create(name="Python")
        self.django = Skill.objects.create(name="Django")
        self.sql = Skill.objects.create(name="SQL")
        self.javascript = Skill.objects.create(name="JavaScript")
        self.react = Skill.objects.create(name="React")

        # Create user with profile
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.create(user=self.user, fullname="Test User")
        self.profile.skills.set([self.python, self.django, self.sql])

        # Create jobs
        self.job1 = Job.objects.create(
            title="Django Developer", company="Tech Corp", job_type="Full-time"
        )
        self.job1.required_skills.set([self.python, self.django, self.sql])

        self.job2 = Job.objects.create(
            title="Python Developer", company="Code Inc", job_type="Full-time"
        )
        self.job2.required_skills.set([self.python])

        self.job3 = Job.objects.create(
            title="Frontend Developer", company="Web Co", job_type="Full-time"
        )
        self.job3.required_skills.set([self.javascript, self.react])

    def test_match_jobs_ranking(self):
        """Jobs should be ranked by match score."""
        jobs_qs = Job.objects.all()
        matches = match_jobs_for_user(self.profile, jobs_qs, limit=10)

        self.assertEqual(len(matches), 3)

        # job1 should be first (100% match)
        self.assertEqual(matches[0]["job_id"], self.job1.id)
        self.assertEqual(matches[0]["match_score"], 1.0)
        self.assertEqual(len(matches[0]["matching_skills"]), 3)

        # job2 should be second (100% match but fewer skills)
        self.assertEqual(matches[1]["job_id"], self.job2.id)
        self.assertEqual(matches[1]["match_score"], 1.0)

        # job3 should be last (0% match)
        self.assertEqual(matches[2]["job_id"], self.job3.id)
        self.assertEqual(matches[2]["match_score"], 0.0)

    def test_match_jobs_limit(self):
        """Should respect the limit parameter."""
        jobs_qs = Job.objects.all()
        matches = match_jobs_for_user(self.profile, jobs_qs, limit=2)
        self.assertEqual(len(matches), 2)

    def test_match_jobs_empty_profile(self):
        """User with no skills should get baseline matches."""
        empty_profile = UserProfile.objects.create(
            user=User.objects.create_user(
                email="empty@example.com", password="testpass123"
            ),
            fullname="Empty User",
        )

        jobs_qs = Job.objects.all()
        matches = match_jobs_for_user(empty_profile, jobs_qs, limit=10)

        # All jobs should have 0.0 match score
        for match in matches:
            self.assertEqual(match["match_score"], 0.0)


class ResourceMatchingTests(TestCase):
    """Tests for learning resource matching logic."""

    def setUp(self):
        """Create test user, skills, and resources."""
        # Create skills
        self.python = Skill.objects.create(name="Python")
        self.django = Skill.objects.create(name="Django")
        self.sql = Skill.objects.create(name="SQL")

        # Create user with profile
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.create(user=self.user, fullname="Test User")
        self.profile.skills.set([self.python, self.django])

        # Create resources
        self.resource1 = LearningResource.objects.create(
            title="Django Tutorial", url="https://example.com/django", cost="Free"
        )
        self.resource1.related_skills.set([self.python, self.django])

        self.resource2 = LearningResource.objects.create(
            title="Python Basics", url="https://example.com/python", cost="Free"
        )
        self.resource2.related_skills.set([self.python])

        self.resource3 = LearningResource.objects.create(
            title="SQL Mastery", url="https://example.com/sql", cost="Paid"
        )
        self.resource3.related_skills.set([self.sql])

    def test_match_resources_ranking(self):
        """Resources should be ranked by match score."""
        resources_qs = LearningResource.objects.all()
        matches = match_resources_for_user(self.profile, resources_qs, limit=10)

        self.assertEqual(len(matches), 3)

        # resource1 should be first (100% match)
        self.assertEqual(matches[0]["resource_id"], self.resource1.id)
        self.assertEqual(matches[0]["match_score"], 1.0)

        # resource2 should be second (100% match but fewer skills)
        self.assertEqual(matches[1]["resource_id"], self.resource2.id)
        self.assertEqual(matches[1]["match_score"], 1.0)

        # resource3 should be last (0% match - no common skills)
        self.assertEqual(matches[2]["resource_id"], self.resource3.id)
        self.assertEqual(matches[2]["match_score"], 0.0)


class DashboardAPITests(TestCase):
    """Tests for dashboard API endpoint."""

    def setUp(self):
        """Create test user with profile, skills, jobs, and resources."""
        # Create skills
        self.python = Skill.objects.create(name="Python")
        self.django = Skill.objects.create(name="Django")

        # Create user
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.profile = UserProfile.objects.create(
            user=self.user, fullname="Test User", bio="Software developer"
        )
        self.profile.skills.set([self.python, self.django])

        # Create job
        self.job = Job.objects.create(
            title="Django Developer", company="Tech Corp", job_type="Full-time"
        )
        self.job.required_skills.set([self.python, self.django])

        # Create resource
        self.resource = LearningResource.objects.create(
            title="Django Tutorial", url="https://example.com/django", cost="Free"
        )
        self.resource.related_skills.set([self.django])

    def test_dashboard_requires_auth(self):
        """Dashboard endpoint requires authentication."""
        response = self.client.get("/api/dashboard")
        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, 401)

    def test_matching_jobs_requires_auth(self):
        """Matching jobs endpoint requires authentication."""
        response = self.client.get("/api/matching/jobs")
        self.assertEqual(response.status_code, 401)

    def test_matching_resources_requires_auth(self):
        """Matching resources endpoint requires authentication."""
        response = self.client.get("/api/matching/resources")
        self.assertEqual(response.status_code, 401)
