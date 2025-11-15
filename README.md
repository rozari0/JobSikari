
# Project Setup

## Environment Setup

- Copy the environment template and edit it with your values:

```bash
cp .env.dist .env
````

## Installation

-  Install dependencies:

```bash
pip install -r requirements.txt
```

- Apply database migrations:

```bash
python manage.py migrate
```

- Collect static for the admin panel:
```zsh
python manage.py collectstatic
```

- Seed initial data:

```bash
python manage.py seed_all
```

- Create a superuser:
```zsh
python manage.py createsuperuser
```

## Running the Project

### Development Server

```bash
python manage.py runserver
```

### Production Server

```bash
gunicorn --workers=2 -b 0.0.0.0:8000 sikari.wsgi
```

## Access

* **API Documentation:** [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
* **Admin Panel:** [http://localhost:8000/docs](http://localhost:8000/docs)


### External APIs Utilized

- Supabase – for S3 storage management

- Gemini – powers the AI CareerBot, providing CV reviews, intelligent skill gap analysis, personalized roadmap generation, and skill extraction from CV

- FLUX.1 Kontext - powers the headshot generator