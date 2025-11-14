import os
import tempfile
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from ninja import File, Form
from ninja.errors import HttpError
from ninja.files import UploadedFile
from ninja_extra import api_controller, http_delete, http_get, http_post
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController
from pypdf import PdfReader

from .models import Careers, GeneratedRoadmap, Project, Skill, User, UserProfile
from .schema import (
    CVSchemaOut,
    ProfileSchema,
    ProjectSchema,
    RegisterUserSchema,
    UpdateProfileSchema,
    UserSchema,
)


@api_controller(tags=["UserAPI"])
class UserAPI:
    @http_get("/users/{username}", response=UserSchema)
    def get_user(self, request, username: str):
        user = get_object_or_404(User, username=username)
        return {
            "id": user.id,
            "fullname": user.profile.fullname,
            "email": user.email,
            "username": user.username,
            "education": user.profile.education,
            "experience": user.profile.experience,
            "skills": [s.name for s in user.profile.skills.all()],
            "preferred_careers": [
                career.title for career in user.profile.preferred_careers.all()
            ],
            "cv_text": user.profile.cv_text,
            "projects": user.projects.all(),
        }

    @http_get(
        "/is_available/{username}",
    )
    def check_username(self, request, username: str):
        if User.objects.filter(username=username).exists():
            return {"available": False}
        return {"available": True}

    @http_get("/set_username/{new_username}", response=UserSchema, auth=JWTAuth())
    def set_username(self, request, new_username: str):
        user = request.user
        if User.objects.filter(username=new_username).exists():
            raise HttpError(400, "Username already taken")
        user.username = new_username
        user.save()
        return {
            "id": user.id,
            "fullname": user.profile.fullname,
            "email": user.email,
        }

    @http_get("/profile", response=ProfileSchema, auth=JWTAuth())
    def get_profile(self, request):
        user = request.user
        profile = user.profile
        return {
            "id": user.id,
            "fullname": profile.fullname,
            "email": user.email,
            "username": user.username,
            "education": profile.education,
            "experience": profile.experience,
            "bio": profile.bio,
            "skills": [s.name for s in profile.skills.all()],
            "preferred_careers": [c.title for c in profile.preferred_careers.all()],
            "cv_text": profile.cv_text,
            "cv_full": profile.cv_full,
            "suggested_roles": [c.title for c in profile.suggested_roles.all()],
            "projects": user.projects.all(),
        }

    @http_post("/profile", response=ProfileSchema, auth=JWTAuth())
    def update_profile(self, request, data: UpdateProfileSchema):
        user = request.user
        profile = user.profile

        if data.fullname is not None:
            profile.fullname = data.fullname
        if data.education is not None:
            profile.education = data.education
        if data.experience is not None:
            profile.experience = data.experience
        if data.bio is not None:
            profile.bio = data.bio
        if data.cv_text is not None:
            profile.cv_text = data.cv_text

        # Skills: accept list of skill names, create if missing
        if data.skills is not None:
            skill_objs = []
            for name in data.skills:
                name = name.strip()
                if not name:
                    continue

                # Try to get by slug first (in case different names slugify to same slug)
                slug = slugify(name)
                skill_obj = None
                try:
                    skill_obj = Skill.objects.get(slug=slug)
                except Skill.DoesNotExist:
                    # Try to get by name (case-insensitive)
                    try:
                        skill_obj = Skill.objects.get(name__iexact=name)
                    except Skill.DoesNotExist:
                        # Create new skill, handling potential slug collisions
                        try:
                            skill_obj, _ = Skill.objects.get_or_create(name=name)
                        except IntegrityError:
                            # If slug collision occurs, get the existing skill by slug
                            skill_obj = Skill.objects.get(slug=slug)

                skill_objs.append(skill_obj)
            profile.skills.set(skill_objs)

        # Preferred careers: accept list of titles
        if data.preferred_careers is not None:
            career_objs = []
            for title in data.preferred_careers:
                title = title.strip()
                if not title:
                    continue
                career_obj, _ = Careers.objects.get_or_create(title=title)
                career_objs.append(career_obj)
            profile.preferred_careers.set(career_objs)

        profile.save()
        return {
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

    @http_get("/skills", auth=JWTAuth())
    def list_skills(self, request):
        skills = request.user.profile.skills.values_list("name", flat=True)
        return {"skills": list(skills)}

    @http_post("/skills", auth=JWTAuth())
    def add_skill(self, request, skill_names: list[str]):
        for skill_name in skill_names:
            skill_name = skill_name.strip()

            slug = slugify(skill_name)
            skill_obj = None
            try:
                Skill.objects.get(slug=slug)
            except Skill.DoesNotExist:
                skill_obj = Skill.objects.create(name=skill_name)

            request.user.profile.skills.add(skill_obj)
        return {"message": "Skill(s) added successfully"}

    @http_delete("/skills", auth=JWTAuth())
    def remove_skill(self, request, skill_name: str):
        skill_name = skill_name.strip()
        slug = slugify(skill_name)
        try:
            skill_obj = Skill.objects.get(slug=slug)
            request.user.profile.skills.remove(skill_obj)
            return {"message": "Skill removed successfully"}
        except Skill.DoesNotExist:
            raise HttpError(404, "Skill not found")

    @http_post("/suggested_roles", auth=JWTAuth())
    def add_suggested_role(self, request, career_titles: list[str]):
        print(career_titles)
        for title in career_titles:
            title = title.strip()
            if not title:
                continue
            career_obj, _ = Careers.objects.get_or_create(title=title.capitalize())
            request.user.profile.suggested_roles.add(career_obj)
        return {"message": "Suggested role(s) added successfully"}

    @http_post("/add_project", auth=JWTAuth())
    def add_project(
        self, request, data: Form[ProjectSchema], file: File[UploadedFile] = None
    ):
        project = Project.objects.create(
            user=request.user,
            title=data.title,
            description=data.description,
            link=data.link,
        )
        if file:
            project.image = file
            project.save()
        return {"message": "Project added successfully", "project_id": project.id}

    @http_delete("/delete_project", auth=JWTAuth())
    def delete_project(self, request, id: int):
        project = get_object_or_404(Project, user=request.user, id=id)
        project.delete()
        return {"message": "Project deleted successfully"}


@api_controller(tags="Register API")
class RegisterAPI:
    @http_post("/register", response=UserSchema)
    def register_user(self, request, data: RegisterUserSchema):
        # Basic validation
        if not data.fullname or not data.fullname.strip():
            raise HttpError(400, "fullname is required")

        try:
            validate_email(data.email)
        except ValidationError:
            raise HttpError(400, "Invalid email format")

        if len(data.password or "") < 8:
            raise HttpError(400, "Password must be at least 8 characters")

        if User.objects.filter(email=data.email).exists():
            raise HttpError(400, "A user with that email already exists")

        user = User.objects.create_user(
            username=str(uuid.uuid4()),
            email=data.email,
            password=data.password,
        )
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            fullname=data.fullname,
        )
        return {
            "id": user.id,
            "fullname": profile.fullname,
            "username": user.username,
            "email": user.email,
        }


class NinjaJWTController(NinjaJWTDefaultController):
    pass


@api_controller(tags=["PDF", "MISCs"])
class PDFController:
    @http_post("/pdf/textify", auth=JWTAuth())
    def textify(self, request, file: File[UploadedFile]):
        try:
            suffix = (
                os.path.splitext(getattr(file, "filename", "upload.pdf"))[1] or ".pdf"
            )
            tmp_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp_path = tmp.name
                    # Try to read from underlying file object, fallback to .read()
                    try:
                        file.file.seek(0)
                        tmp.write(file.file.read())
                    except Exception:
                        tmp.write(file.read())

                reader = PdfReader(tmp_path)
                text_parts = []
                for page in reader.pages:
                    text_parts.append(page.extract_text() or "")

                request.user.profile.cv_full = "\n".join(text_parts).strip()
                request.user.profile.save()
                return {"text": "\n".join(text_parts).strip()}
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass
        except Exception as e:
            raise HttpError(400, f"Failed to extract text from PDF: {str(e)}")

    @http_get("/roadmap/get", auth=JWTAuth(), response=CVSchemaOut)
    def get_user_cv(self, request):
        cv, _ = GeneratedRoadmap.objects.get_or_create(
            user=request.user,
        )
        return cv

    @http_post("/roadmap/save", auth=JWTAuth(), response=CVSchemaOut)
    def save_user_cv(self, request, file: File[UploadedFile]):
        cv, _ = GeneratedRoadmap.objects.get_or_create(
            user=request.user,
        )
        cv.file = file
        cv.save()

        return cv
