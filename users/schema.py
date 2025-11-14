from typing import Optional

from ninja import Schema


class ProjectSchema(Schema):
    title: str
    description: str | None = None
    link: str | None = None


class ProjectOutSchema(ProjectSchema):
    id: int
    image: str | None = None


class UserSchema(Schema):
    id: int
    fullname: str
    email: str
    username: Optional[str] = None
    education: str | None = None
    experience: str | None = None
    skills: list[str] | None = None
    preferred_careers: list[str] | None = None
    cv_text: Optional[str] = None
    projects: list[ProjectOutSchema] | None = None


class RegisterUserSchema(Schema):
    fullname: str
    email: str
    password: str


class ProfileSchema(Schema):
    id: int
    fullname: str
    email: str
    username: Optional[str] = None
    education: str | None = None
    experience: str | None = None
    bio: str | None = None
    skills: list[str] | None = None
    preferred_careers: list[str] | None = None
    cv_text: str | None = None
    cv_full: str | None = None
    suggested_roles: list[str] | None = None
    projects: list[ProjectOutSchema] | None = None


class UpdateProfileSchema(Schema):
    fullname: str | None = None
    education: str | None = None
    experience: str | None = None
    bio: str | None = None
    skills: list[str] | None = None
    preferred_careers: list[str] | None = None
    suggested_roles: list[str] | None = None
    cv_text: str | None = None


class CVSchemaOut(Schema):
    file: str | None = None
