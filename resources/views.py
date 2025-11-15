from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from ninja_extra import api_controller, http_get, http_post
from django.views.decorators.cache import cache_page

from users.models import Skill

from .filters import ResourceFilter
from .models import LearningResource
from .schema import CreateLearningResourceSchema, LearningResourceSchema


@api_controller
class ResourcesAPI:
    @cache_page(60)
    @http_get("/resources", response=list[LearningResourceSchema])
    def list_resources(
        self,
        request,
        skill: str | None = None,
        cost: str | None = None,
        platform: str | None = None,
    ):
        # Use django-filter (required)
        qs = ResourceFilter(
            data={"skill": skill, "cost": cost, "platform": platform},
            queryset=LearningResource.objects.all(),
        ).qs
        results = []
        for r in qs.distinct():
            results.append({
                "id": r.id,
                "title": r.title,
                "platform": r.platform,
                "url": r.url,
                "related_skills": [s.name for s in r.related_skills.all()],
                "cost": r.cost,
                "description": r.description,
            })
        return results

    @cache_page(60)
    @http_get("/resources/{resource_id}", response=LearningResourceSchema)
    def get_resource(self, request, resource_id: int):
        resource = get_object_or_404(LearningResource, pk=resource_id)
        return {
            "id": resource.id,
            "title": resource.title,
            "platform": resource.platform,
            "url": resource.url,
            "related_skills": [s.name for s in resource.related_skills.all()],
            "cost": resource.cost,
            "description": resource.description,
        }

    @http_post("/resources", response=LearningResourceSchema)
    def create_resource(self, request, data: CreateLearningResourceSchema):
        # basic creation endpoint (no auth for now)
        if LearningResource.objects.filter(title=data.title, url=data.url).exists():
            raise HttpError(400, "Resource already exists")
        r = LearningResource.objects.create(
            title=data.title,
            platform=data.platform,
            url=data.url,
            cost=(data.cost or "Free"),
            description=data.description,
        )
        if data.related_skills:
            skill_objs = []
            for name in data.related_skills:
                name = name.strip()
                if not name:
                    continue
                skill_obj, _ = Skill.objects.get_or_create(name=name)
                skill_objs.append(skill_obj)
            r.related_skills.set(skill_objs)
        return {
            "id": r.id,
            "title": r.title,
            "platform": r.platform,
            "url": r.url,
            "related_skills": [s.name for s in r.related_skills.all()],
            "cost": r.cost,
            "description": r.description,
        }
