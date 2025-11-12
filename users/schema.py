from ninja import Schema


class UserSchema(Schema):
    id: int
    fullname: str
    email: str
    education: str | None = None
    experience: str | None = None
    skills: list[str] | None = None
    preferred_careers: list[str] | None = None


class RegisterUserSchema(Schema):
    fullname: str
    email: str
    password: str
