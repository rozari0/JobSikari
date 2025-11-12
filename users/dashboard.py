"""
Matching and Dashboard API controllers for JobSikari.

Provides endpoints for skill-based job/resource recommendations
and a unified dashboard view for authenticated users.
"""

from ninja_extra import api_controller, http_get
from ninja_jwt.authentication import JWTAuth

from jobs.models import Job
from jobs.schema import JobRecommendationSchema
from resources.models import LearningResource
from resources.schema import ResourceRecommendationSchema
from users.matching import match_jobs_for_user, match_resources_for_user
from users.schema import ProfileSchema


@api_controller
class MatchingAPI:
    """API endpoints for personalized job and resource matching."""

    @http_get("/matching/jobs", response=list[JobRecommendationSchema], auth=JWTAuth())
    def recommended_jobs(self, request, limit: int = 10):
        """
        Get recommended jobs based on user's skill profile.

        Returns jobs ranked by skill overlap with the authenticated user's profile.
        """
        user = request.user
        profile = user.profile

        jobs_qs = Job.objects.prefetch_related("required_skills").all()
        matches = match_jobs_for_user(profile, jobs_qs, limit=limit)

        results = []
        for match in matches:
            job = Job.objects.prefetch_related("required_skills").get(
                id=match["job_id"]
            )
            results.append(
                {
                    "job": {
                        "id": job.id,
                        "title": job.title,
                        "company": job.company,
                        "location": job.location,
                        "is_remote": job.is_remote,
                        "required_skills": [s.name for s in job.required_skills.all()],
                        "recommended_experience": job.recommended_experience,
                        "job_type": job.job_type,
                        "description": job.description,
                        "posted_at": job.posted_at.isoformat(),
                    },
                    "match_score": match["match_score"],
                    "matching_skills": match["matching_skills"],
                }
            )

        return results

    @http_get(
        "/matching/resources",
        response=list[ResourceRecommendationSchema],
        auth=JWTAuth(),
    )
    def recommended_resources(self, request, limit: int = 10):
        """
        Get recommended learning resources based on user's skill profile.

        Returns resources ranked by skill overlap with the authenticated user's profile.
        """
        user = request.user
        profile = user.profile

        resources_qs = LearningResource.objects.prefetch_related("related_skills").all()
        matches = match_resources_for_user(profile, resources_qs, limit=limit)

        results = []
        for match in matches:
            resource = LearningResource.objects.prefetch_related("related_skills").get(
                id=match["resource_id"]
            )
            results.append(
                {
                    "resource": {
                        "id": resource.id,
                        "title": resource.title,
                        "platform": resource.platform,
                        "url": resource.url,
                        "related_skills": [
                            s.name for s in resource.related_skills.all()
                        ],
                        "cost": resource.cost,
                        "description": resource.description,
                    },
                    "match_score": match["match_score"],
                    "matching_skills": match["matching_skills"],
                }
            )

        return results


class DashboardResponse:
    """Response schema for dashboard endpoint."""

    profile: ProfileSchema
    recommended_jobs: list[JobRecommendationSchema]
    recommended_resources: list[ResourceRecommendationSchema]


@api_controller
class DashboardAPI:
    """Unified dashboard API for authenticated users."""

    @http_get("/dashboard", auth=JWTAuth())
    def get_dashboard(self, request):
        """
        Get user dashboard with profile and personalized recommendations.

        Returns:
            - User profile information
            - Top 5 recommended jobs based on skills
            - Top 5 recommended learning resources based on skills
        """
        user = request.user
        profile = user.profile

        # Get profile data
        profile_data = {
            "id": user.id,
            "fullname": profile.fullname,
            "email": user.email,
            "education": profile.education,
            "experience": profile.experience,
            "bio": profile.bio,
            "skills": [s.name for s in profile.skills.all()],
            "preferred_careers": [c.title for c in profile.preferred_careers.all()],
            "cv_text": profile.cv_text,
        }

        # Get recommended jobs
        jobs_qs = Job.objects.prefetch_related("required_skills").all()
        job_matches = match_jobs_for_user(profile, jobs_qs, limit=5)

        recommended_jobs = []
        for match in job_matches:
            job = Job.objects.prefetch_related("required_skills").get(
                id=match["job_id"]
            )
            recommended_jobs.append(
                {
                    "job": {
                        "id": job.id,
                        "title": job.title,
                        "company": job.company,
                        "location": job.location,
                        "is_remote": job.is_remote,
                        "required_skills": [s.name for s in job.required_skills.all()],
                        "recommended_experience": job.recommended_experience,
                        "job_type": job.job_type,
                        "description": job.description,
                        "posted_at": job.posted_at.isoformat(),
                    },
                    "match_score": match["match_score"],
                    "matching_skills": match["matching_skills"],
                }
            )

        # Get recommended resources
        resources_qs = LearningResource.objects.prefetch_related("related_skills").all()
        resource_matches = match_resources_for_user(profile, resources_qs, limit=5)

        recommended_resources = []
        for match in resource_matches:
            resource = LearningResource.objects.prefetch_related("related_skills").get(
                id=match["resource_id"]
            )
            recommended_resources.append(
                {
                    "resource": {
                        "id": resource.id,
                        "title": resource.title,
                        "platform": resource.platform,
                        "url": resource.url,
                        "related_skills": [
                            s.name for s in resource.related_skills.all()
                        ],
                        "cost": resource.cost,
                        "description": resource.description,
                    },
                    "match_score": match["match_score"],
                    "matching_skills": match["matching_skills"],
                }
            )

        return {
            "profile": profile_data,
            "recommended_jobs": recommended_jobs,
            "recommended_resources": recommended_resources,
        }
