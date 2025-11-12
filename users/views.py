import uuid

from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from ninja_extra import api_controller, http_get, http_post
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

from .models import User, UserProfile
from .schema import RegisterUserSchema, UserSchema


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


@api_controller()
class RegisterAPI:
    @http_post("/register", response=UserSchema)
    def register_user(self, request, data: RegisterUserSchema):
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
