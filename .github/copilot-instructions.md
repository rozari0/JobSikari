<!-- Copilot / AI agent guidance for JobSikari -->
# Project guidance for AI coding agents

This repository is a small Django project exposing a Ninja API and a custom user app. The file-level examples below are intentionally specific so an AI agent can be productive immediately.

- Architecture (big picture)
  - Django project root: `sikari/` (settings, wsgi/asgi, urls).
  - Main API registration: `sikari/api.py` registers controllers from `users.views` using `NinjaExtraAPI`.
  - App: `users/` contains the custom `User` model, profile, API controllers, schemas, and managers.
  - Database: sqlite by default (`db.sqlite3`), configured in `sikari/settings.py`.

- Important patterns & conventions
  - Auth model: `users.models.User` is a custom user where `USERNAME_FIELD = "email"` and `AUTH_USER_MODEL = "users.User"` (see `sikari/settings.py`). Many user-facing endpoints rely on `user.profile` (OneToOne `UserProfile`).
  - Managers: `users.managers.CustomUserManager` must be used for creating users and superusers — use `create_user` / `create_superuser`.
  - Lifecycle hooks: models use `django_lifecycle` (e.g., `Skill.set_slug` uses `@hook(BEFORE_CREATE)`). Prefer to preserve those hooks when modifying models.
  - API controllers: use `ninja_extra` controllers in `users/views.py` with decorators `@api_controller`, `@http_get`, `@http_post`. Response shapes use `users/schema.py` (Ninja `Schema`).
  - JWT auth: `ninja_jwt` is used. Example: `@http_get(..., auth=JWTAuth())` and a controller `class NinjaJWTController(NinjaJWTDefaultController)` is present.
  - Username policy: username is optional and sometimes generated as a UUID at registration (`RegisterAPI.register_user`). When changing username, check uniqueness (`User.objects.filter(username=...).exists()`).

- Key example endpoints (copyable references)
  - GET /users/{username} -> `UserAPI.get_user` in `users/views.py` (returns `UserSchema`).
  - POST /register -> `RegisterAPI.register_user` (creates a `User` with `username=str(uuid.uuid4())`).
  - GET /set_username/{new_username} (authenticated via JWT) updates `request.user.username` after checking uniqueness.

- Developer workflows (commands you can safely run locally)
  - Run dev server: `python manage.py runserver`
  - Migrations: `python manage.py makemigrations` then `python manage.py migrate`
  - Create superuser: `python manage.py createsuperuser`
  - Run tests: `python manage.py test` (tests live in `users/tests.py`)
  - Dependency hint: dependencies are listed in `pyproject.toml` under `[project].dependencies` (examples: `django`, `django-lifecycle`, `django-ninja`, `django-ninja-extra`, `django-ninja-jwt`). Install with pip if no environment manager is used.

- Files of interest (fast map)
  - `sikari/settings.py` — DB, INSTALLED_APPS, `AUTH_USER_MODEL`, timezone, DEBUG.
  - `sikari/api.py` — where API controllers are registered.
  - `users/views.py` — primary API controllers and routes.
  - `users/models.py` — `User`, `UserProfile`, `Skill`, `Careers` (lifecycle hooks, relations).
  - `users/schema.py` — Ninja `Schema` types used for responses and request validation.
  - `users/managers.py` — custom user creation logic.
  - `users/migrations/` — migration history that must be preserved.

- Edits and PR guidance (project-specific)
  - When changing the user model or manager, ensure `create_superuser` still sets `is_staff` and `is_superuser` (see existing `CustomUserManager`).
  - Keep lifecycle hooks intact when altering model fields that affect slugs or related collections.
  - If adding API routes, register controllers via `sikari/api.py` (follow the `NinjaExtraAPI` pattern).
  - Run migrations and tests locally before opening a PR.

- Quick debugging tips
  - Use `python manage.py shell` and `from users.models import User; User.objects.get(email=...)` to inspect users and `user.profile` for profile data.
  - The project uses sqlite by default (`db.sqlite3`) — it's fine for local debugging; don't assume production DB features.
  - If authentication issues appear, verify `AUTH_USER_MODEL` and `USERNAME_FIELD` in `users/models.py` and `sikari/settings.py`.

If anything here is unclear or you'd like more examples (e.g., example tests, expanded API route map, or environment setup steps for Poetry/virtualenv), tell me which area to expand and I'll iterate.
