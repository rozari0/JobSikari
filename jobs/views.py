import requests
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from ninja_extra import api_controller, http_get, http_post
from yt_dlp import YoutubeDL

from users.models import Skill

from .filters import JobFilter
from .models import Job
from .schema import BDJobSchema, CreateJobSchema, JobSchema, YouTubeSearchResult


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
            results.append(
                {
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
            )
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


def youtube_search(query, limit=5):
    """
    Perform a YouTube search with yt-dlp and return the first `limit` results.
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,  # prevents full metadata download
    }

    search_query = f"ytsearch{limit}:{query}"

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=False)

    results = []
    for entry in info.get("entries", [])[:limit]:
        results.append(
            {
                "title": entry.get("title"),
                "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                "thumbnail": f"https://img.youtube.com/vi/{entry.get('id')}/default.jpg",
                "channel": entry.get("channel"),
                "duration": entry.get("duration"),
            }
        )

    return results


@api_controller()
class ExternalJobs:
    @http_get("/bdjobs/search", response=list[BDJobSchema])
    def fetch_bdjobs(self, request, query: str):
        response = requests.get(
            f"https://api.bdjobs.com/Jobs/api/JobSearch/GetJobSearch?isPro=1&rpp=50&pg=1&keyword={query}"
        )

        return [
            {
                "id": job["Jobid"],
                "title": job["jobTitle"],
                "company": job["companyName"],
                "location": job["location"],
                "is_remote": job.get("OnlineJob", False),
                "recommended_experience": job["experience"],
                "description": job["jobContext"],
                "deadline": job["deadline"],
            }
            for job in response.json().get("data", [])[:5]
        ]

    @http_get("/youtube/search", response=list[YouTubeSearchResult])
    def youtube_search_endpoint(self, request, query: str, limit: int = 5):
        return youtube_search(query, limit)
