import uuid

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from ninja.errors import HttpError
from ninja_extra import api_controller, http_get, http_post
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

from .models import Careers, Skill, User, UserProfile
from .schema import ProfileSchema, RegisterUserSchema, UpdateProfileSchema, UserSchema


@api_controller
class UserAPI:
    @http_get("/users/{username}", response=UserSchema)
    def get_user(self, request, username: str):
        user = get_object_or_404(User, username=username)
        return {
            "id": user.id,
            "fullname": user.profile.fullname,
            "email": user.email,
            "education": user.profile.education,
            "experience": user.profile.experience,
            "skills": user.profile.skills,
            "preferred_careers": user.profile.preferred_careers,
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
            "education": profile.education,
            "experience": profile.experience,
            "bio": profile.bio,
            "skills": [s.name for s in profile.skills.all()],
            "preferred_careers": [c.title for c in profile.preferred_careers.all()],
            "cv_text": profile.cv_text,
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


@api_controller()
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
