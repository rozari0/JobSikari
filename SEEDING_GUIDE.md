# Database Seeding Scripts

This folder contains Django management commands to populate the database with sample data.

## Available Commands

### 1. Seed All Data (Recommended)
Seeds both jobs and learning resources in one command:

```bash
python manage.py seed_all
```

**Options:**
- `--clear` - Clear existing data before seeding

```bash
python manage.py seed_all --clear
```

### 2. Seed Jobs Only
Seeds 20 entry-level job postings:

```bash
python manage.py seed_jobs
```

**Options:**
- `--clear` - Clear existing jobs before seeding

```bash
python manage.py seed_jobs --clear
```

**Sample Jobs Include:**
- Junior Python Developer
- Frontend Developer Intern
- Entry Level Full Stack Developer
- Junior Backend Engineer
- And 16 more...

**Job Details:**
- Title, Company, Location
- Remote/On-site flag
- Job type (Full-time, Part-time, Internship)
- Required skills (linked to Skill model)
- Experience level recommendations
- Full descriptions

### 3. Seed Learning Resources Only
Seeds 25 learning resources (courses, tutorials, articles):

```bash
python manage.py seed_resources
```

**Options:**
- `--clear` - Clear existing resources before seeding

```bash
python manage.py seed_resources --clear
```

**Sample Resources Include:**
- Python for Beginners - Complete Course (YouTube)
- Django Web Framework Tutorial (freeCodeCamp)
- The Complete JavaScript Course (Udemy)
- React - The Complete Guide (Udemy)
- CS50's Introduction to Computer Science (Harvard)
- And 20 more...

**Resource Details:**
- Title, Platform, URL
- Cost (Free/Paid)
- Related skills (linked to Skill model)
- Descriptions

## Skills Created

The seeding commands automatically create and link skills including:

**Programming Languages:**
- Python, JavaScript, TypeScript, Java, C#, Ruby, PHP

**Frameworks:**
- Django, Flask, FastAPI, React, Vue.js, Node.js, Spring Boot, .NET, Rails, Laravel

**Databases:**
- SQL, PostgreSQL, MySQL, MongoDB

**Tools & Technologies:**
- Git, Docker, AWS, Azure, REST API, GraphQL, Testing, Agile

**Other:**
- HTML, CSS, Tailwind CSS, Bootstrap, Data Analysis, Excel, Tableau, Power BI

## Usage Workflow

### First Time Setup

1. **Run migrations** (if not already done):
   ```bash
   python manage.py migrate
   ```

2. **Seed all data**:
   ```bash
   python manage.py seed_all
   ```

3. **Verify the data**:
   ```bash
   python manage.py shell -c "from jobs.models import Job; from resources.models import LearningResource; print(f'Jobs: {Job.objects.count()}'); print(f'Resources: {LearningResource.objects.count()}')"
   ```

### Re-seeding (Development)

If you want to start fresh:

```bash
python manage.py seed_all --clear
```

This will:
1. Delete all existing jobs and resources
2. Create fresh data

**Note:** Skills are never deleted, they're reused if they already exist.

## Data Statistics

After running `seed_all`:
- **Jobs:** 20 entry-level positions
- **Resources:** 25 learning resources
- **Skills:** ~40 unique skills
- **Companies:** 20 different companies
- **Platforms:** YouTube, Udemy, freeCodeCamp, Harvard, Google, AWS, etc.

## File Structure

```
jobs/
  management/
    commands/
      seed_jobs.py         # Seeds job postings
resources/
  management/
    commands/
      seed_resources.py    # Seeds learning resources
users/
  management/
    commands/
      seed_all.py          # Seeds everything at once
```

## Integration with API

Once seeded, the data is immediately available through the API endpoints:

- **GET /api/jobs** - List all jobs
- **GET /api/resources** - List all resources
- **GET /api/matching/jobs** - Get recommended jobs (requires JWT)
- **GET /api/matching/resources** - Get recommended resources (requires JWT)
- **GET /api/dashboard** - Get dashboard with recommendations (requires JWT)

## Customization

To add more data:

1. Edit `seed_jobs.py` or `seed_resources.py`
2. Add entries to the `jobs_data` or `resources_data` list
3. Run the seeding command again

The commands use `get_or_create()` to avoid duplicates based on:
- Jobs: `title` + `company`
- Resources: `title` + `url`

## Testing

The seed commands include color-coded output:
- ✓ **Green** - Successfully created new item
- ⊙ **White** - Item already exists (skipped)
- **Blue** - Section headers
- **Yellow** - Summary information

## Notes

- Skills are shared across jobs and resources
- Running seed commands multiple times is safe (idempotent)
- Use `--clear` flag carefully - it deletes existing data
- All data includes realistic descriptions and details
- Jobs include a mix of remote and on-site positions
- Resources include both free and paid options
