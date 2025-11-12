from django.shortcuts import get_object_or_404
from ninja_extra import api_controller, http_get, http_post
from django.db import models
from ninja.errors import HttpError
from .filters import JobFilter

from .models import Job
from .schema import JobSchema, CreateJobSchema
from users.models import Skill


@api_controller
class JobsAPI:
    @http_get("/jobs", response=list[JobSchema])
    def list_jobs(
        self,
        request,
        skill: str | None = None,
        location: str | None = None,
        job_type: str | None = None,
    ):
        qs = Job.objects.all()
        # Use django-filter (required)
        qs = JobFilter(
            data={"skill": skill, "location": location, "job_type": job_type},
            queryset=qs,
        ).qs
        # interpret "remote" location specially
        if location and location.lower() == "remote":
            qs = qs.filter(is_remote=True)
        results = []
        for j in qs.distinct().order_by("-posted_at"):
            results.append({
                "id": j.id,
                "title": j.title,
                "company": j.company,
                "location": j.location,
                "is_remote": j.is_remote,
                "required_skills": [s.name for s in j.required_skills.all()],
                "recommended_experience": j.recommended_experience,
                "job_type": j.job_type,
                "description": j.description,
                "posted_at": j.posted_at.isoformat(),
            })
        return results

    @http_get("/jobs/{job_id}", response=JobSchema)
    def get_job(self, request, job_id: int):
        job = get_object_or_404(Job, pk=job_id)
        return {
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
        }

    @http_post("/jobs", response=JobSchema)
    def create_job(self, request, data: CreateJobSchema):
        # basic create endpoint (no auth)
        if Job.objects.filter(title=data.title, company=data.company).exists():
            raise HttpError(400, "Job already exists")
        j = Job.objects.create(
            title=data.title,
            company=data.company,
            location=data.location,
            is_remote=bool(data.is_remote),
            recommended_experience=data.recommended_experience,
            job_type=(data.job_type or Job.JobType.FULL_TIME),
            description=data.description,
        )
        if data.required_skills:
            skill_objs = []
            for name in data.required_skills:
                name = name.strip()
                if not name:
                    continue
                skill_obj, _ = Skill.objects.get_or_create(name=name)
                skill_objs.append(skill_obj)
            j.required_skills.set(skill_objs)
        return {
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "is_remote": j.is_remote,
            "required_skills": [s.name for s in j.required_skills.all()],
            "recommended_experience": j.recommended_experience,
            "job_type": j.job_type,
            "description": j.description,
            "posted_at": j.posted_at.isoformat(),
        }
