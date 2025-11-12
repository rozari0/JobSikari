# TODO

This file mirrors the current tracked todo list for the project.

- [x] Create todo list — Record plan and track progress for generating `.github/copilot-instructions.md`
- [x] Search repo for AI instruction files — Find existing AI instruction files to merge
- [x] Open key project files — Read settings, api, users views/models/managers/schema
- [x] Draft `.github/copilot-instructions.md` — Write concise, actionable instructions
- [x] Merge with existing instructions (if any)
- [x] Apply patch to add/update `.github/copilot-instructions.md`
- [ ] Ask for feedback — Prompt for unclear or incomplete sections to iterate
- [x] Audit current implementation vs requested features — Map requested features to codebase

## Implementation Status Summary

**Completed: 13/14 backend tasks (93%)**
**Remaining: 1/14 backend tasks (7%)**

**Note:** Frontend is out of scope - handled separately as a Next.js app

### 2. Registration and profile ✅ COMPLETE (3/3)
   - [x] Improve registration validation (email format, password >= 8 chars, fullname required)
     - ✅ Implemented in `users/views.py` RegisterAPI.register_user with validation
     - ✅ Tests exist in `users/tests.py` RegistrationApiTests
   - [x] Add `cv_text` / `notes` field to `UserProfile` and create migrations
     - ✅ Field added to UserProfile model in `users/models.py`
     - ✅ Migration exists: `users/migrations/0004_add_cv_text.py`
   - [x] Create Profile GET/PATCH endpoints and skill add/remove API
     - ✅ GET /profile endpoint in UserAPI.get_profile (JWT auth)
     - ✅ POST /profile endpoint in UserAPI.update_profile (handles skills, cv_text, etc.)

### 3. Jobs & Resources ✅ COMPLETE (4/4)
   - [x] Add `Job` model + migration (title, company, location, skills M2M, experience level, job_type, remote flag)
     - ✅ Model exists in `jobs/models.py` with all required fields
     - ✅ Migration exists: `jobs/migrations/0001_initial.py`
   - [x] Seed 15–20 entry-level job records (management command or data migration)
     - ✅ Migrations run successfully
     - ✅ Seed command created: `python manage.py seed_jobs` (creates 20 jobs)
     - ✅ 20 jobs seeded with real companies, locations, skills, and descriptions
   - [x] Add `LearningResource` model + migration and seed 15–20 resources
     - ✅ Model exists in `resources/models.py`
     - ✅ Migration exists: `resources/migrations/0001_initial.py`
     - ✅ Seed command created: `python manage.py seed_resources` (creates 25 resources)
     - ✅ 25 resources seeded with platforms (YouTube, Udemy, freeCodeCamp, etc.)
   - [x] Implement Jobs/Resources list & detail APIs with basic filters
     - ✅ JobsAPI in `jobs/views.py`: GET /jobs (with filters), GET /jobs/{id}, POST /jobs
     - ✅ ResourcesAPI in `resources/views.py`: GET /resources (with filters), GET /resources/{id}, POST /resources
     - ✅ Both registered in `sikari/api.py`

### 4. Matching & Dashboard ✅ COMPLETE (2/2)
   - [x] Implement non-AI matching logic (skill overlap) and endpoints
     - ✅ Matching logic implemented in `users/matching.py`
     - ✅ Functions: `calculate_skill_overlap`, `match_jobs_for_user`, `match_resources_for_user`
     - ✅ GET /matching/jobs endpoint (JWT auth required)
     - ✅ GET /matching/resources endpoint (JWT auth required)
   - [x] Create Dashboard API for authenticated users (profile, recommended jobs/resources)
     - ✅ GET /dashboard endpoint in `users/dashboard.py` (JWT auth required)
     - ✅ Returns profile + top 5 recommended jobs + top 5 recommended resources
     - ✅ All controllers registered in `sikari/api.py`

### 5. Docs & tests ⚠️ PARTIAL (1/2)
   - [ ] Add `README.md` with overview, tech stack, setup, seed usage
     - ❌ No README.md found in project root
   - [x] Add unit tests for the new features (registration, profile, jobs/resources, matching)
     - ✅ Registration tests exist in `users/tests.py`
     - ✅ Matching tests exist in `users/test_matching.py` (12 tests, all passing)
     - ✅ Tests cover: skill overlap, job matching, resource matching, dashboard auth
     - ❌ No tests found for profile update, jobs CRUD, resources CRUD

### 6. Frontend / UI ⚠️ OUT OF SCOPE
   - [x] Decide between Django templates vs separate frontend and add basic scaffolding
     - ✅ Decision made: Separate Next.js app (handled by another team member)
     - ✅ Django backend provides REST API only
     - ✅ CORS and authentication configured for external frontend

## Seed Data Commands

Three management commands available for populating the database:

1. **Seed Everything** (Recommended):
   ```bash
   python manage.py seed_all
   ```

2. **Seed Jobs Only**:
   ```bash
   python manage.py seed_jobs
   ```

3. **Seed Resources Only**:
   ```bash
   python manage.py seed_resources
   ```

**Options:** Add `--clear` flag to delete existing data first

**Seeded Data:**
- ✅ 20 entry-level job postings
- ✅ 25 learning resources (free & paid)
- ✅ 40+ skills automatically created and linked

See `SEEDING_GUIDE.md` for complete documentation.

## Next Steps

Remaining backend tasks:
1. ✅ ~~Run migrations~~ - DONE
2. ✅ ~~Create seed data management commands~~ - DONE
3. ✅ ~~Implement matching logic~~ - DONE
4. ✅ ~~Create dashboard API~~ - DONE
5. ❌ Add README.md documentation (only task remaining!)
6. ⚠️  Add more tests for jobs CRUD, resources CRUD, profile update (optional)

## API Endpoints Summary

All endpoints available for frontend integration:

**Authentication:**
- POST /api/register - User registration
- POST /api/token/pair - Get JWT tokens
- POST /api/token/refresh - Refresh access token

**User Profile:**
- GET /api/profile - Get current user profile (JWT)
- POST /api/profile - Update profile with skills (JWT)
- GET /api/users/{username} - Get user by username
- GET /api/set_username/{new_username} - Set username (JWT)

**Jobs:**
- GET /api/jobs - List jobs with filters (skill, location, job_type)
- GET /api/jobs/{id} - Get job details
- POST /api/jobs - Create job

**Resources:**
- GET /api/resources - List resources with filters (skill, cost, platform)
- GET /api/resources/{id} - Get resource details
- POST /api/resources - Create resource

**Matching & Dashboard:**
- GET /api/matching/jobs?limit=10 - Recommended jobs (JWT)
- GET /api/matching/resources?limit=10 - Recommended resources (JWT)
- GET /api/dashboard - Full dashboard with profile + recommendations (JWT)