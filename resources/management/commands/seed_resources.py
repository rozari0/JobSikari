"""
Management command to seed the database with learning resources.

Usage:
    python manage.py seed_resources
    python manage.py seed_resources --clear  # Clear existing resources first
"""

from django.core.management.base import BaseCommand

from resources.models import LearningResource
from users.models import Skill


class Command(BaseCommand):
    help = "Seed the database with learning resources"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing resources before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing resources...")
            LearningResource.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("✓ Cleared all resources"))

        self.stdout.write("Creating/verifying skills...")
        skills_data = [
            "Python",
            "Django",
            "Flask",
            "FastAPI",
            "JavaScript",
            "TypeScript",
            "React",
            "Vue.js",
            "Node.js",
            "HTML",
            "CSS",
            "Tailwind CSS",
            "Bootstrap",
            "SQL",
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "Git",
            "Docker",
            "AWS",
            "Azure",
            "REST API",
            "GraphQL",
            "Testing",
            "Agile",
            "Java",
            "Spring Boot",
            "C#",
            ".NET",
            "Ruby",
            "Rails",
            "PHP",
            "Laravel",
            "Data Analysis",
            "Excel",
            "Tableau",
            "Power BI",
            "Data Science",
            "Machine Learning",
            "Algorithms",
        ]

        skills = {}
        for skill_name in skills_data:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            skills[skill_name] = skill

        self.stdout.write(
            self.style.SUCCESS(f"✓ Created/verified {len(skills)} skills")
        )

        self.stdout.write("Seeding learning resources...")

        resources_data = [
            {
                "title": "Python for Beginners - Complete Course",
                "platform": "YouTube",
                "url": "https://www.youtube.com/watch?v=rfscVS0vtbw",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["Python"],
                "description": "Comprehensive free Python course covering all the basics. Perfect for complete beginners.",
            },
            {
                "title": "Django Web Framework Tutorial",
                "platform": "freeCodeCamp",
                "url": "https://www.freecodecamp.org/news/django-tutorial/",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["Python", "Django"],
                "description": "Learn Django by building real projects. Free comprehensive tutorial series.",
            },
            {
                "title": "The Complete JavaScript Course 2024",
                "platform": "Udemy",
                "url": "https://www.udemy.com/course/the-complete-javascript-course/",
                "cost": LearningResource.CostChoices.PAID,
                "skills": ["JavaScript"],
                "description": "Master JavaScript with the most complete course. Includes ES6+, projects, and more.",
            },
            {
                "title": "React - The Complete Guide",
                "platform": "Udemy",
                "url": "https://www.udemy.com/course/react-the-complete-guide/",
                "cost": LearningResource.CostChoices.PAID,
                "skills": ["React", "JavaScript"],
                "description": "Dive deep into React. Learn Hooks, Redux, Next.js, and more. Build real projects.",
            },
            {
                "title": "CS50's Introduction to Computer Science",
                "platform": "Harvard Online",
                "url": "https://cs50.harvard.edu/x/",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["Python", "Algorithms", "C#"],
                "description": "Harvard's famous intro to CS. Learn programming fundamentals and problem-solving.",
            },
            {
                "title": "SQL for Data Analysis",
                "platform": "Mode Analytics",
                "url": "https://mode.com/sql-tutorial/",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["SQL"],
                "description": "Free interactive SQL tutorial. Learn by doing with real datasets.",
            },
            {
                "title": "Git & GitHub Crash Course",
                "platform": "YouTube",
                "url": "https://www.youtube.com/watch?v=RGOj5yH7evk",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["Git"],
                "description": "Learn Git and GitHub in one hour. Essential version control skills for developers.",
            },
            {
                "title": "Node.js Tutorial for Beginners",
                "platform": "YouTube",
                "url": "https://www.youtube.com/watch?v=TlB_eWDSMt4",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["Node.js", "JavaScript"],
                "description": "Complete Node.js course for beginners. Learn backend development with JavaScript.",
            },
            {
                "title": "Docker for Beginners",
                "platform": "Docker",
                "url": "https://docker-curriculum.com/",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["Docker"],
                "description": "Learn Docker from scratch. Understand containers and how to deploy applications.",
            },
            {
                "title": "REST API Design Best Practices",
                "platform": "Medium",
                "url": "https://medium.com/@schneidenbach/restful-api-best-practices-and-common-pitfalls-7a83ba3763b5",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["REST API"],
                "description": "Article covering REST API design patterns and best practices.",
            },
            {
                "title": "TypeScript Course for Beginners",
                "platform": "YouTube",
                "url": "https://www.youtube.com/watch?v=BwuLxPH8IDs",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["TypeScript", "JavaScript"],
                "description": "Learn TypeScript from scratch. Understand static typing and modern JavaScript.",
            },
            {
                "title": "FastAPI Tutorial",
                "platform": "FastAPI Docs",
                "url": "https://fastapi.tiangolo.com/tutorial/",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["Python", "FastAPI", "REST API"],
                "description": "Official FastAPI tutorial. Build modern, fast web APIs with Python.",
            },
            {
                "title": "Tailwind CSS Crash Course",
                "platform": "YouTube",
                "url": "https://www.youtube.com/watch?v=UBOj6rqRUME",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["Tailwind CSS", "CSS"],
                "description": "Learn utility-first CSS with Tailwind. Build beautiful UIs quickly.",
            },
            {
                "title": "AWS Certified Cloud Practitioner",
                "platform": "AWS Training",
                "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["AWS"],
                "description": "Free AWS fundamentals course. Learn cloud computing basics.",
            },
            {
                "title": "Vue.js 3 - The Complete Guide",
                "platform": "Udemy",
                "url": "https://www.udemy.com/course/vuejs-2-the-complete-guide/",
                "cost": LearningResource.CostChoices.PAID,
                "skills": ["Vue.js", "JavaScript"],
                "description": "Master Vue.js 3. Learn the progressive JavaScript framework from the ground up.",
            },
            {
                "title": "MongoDB University Courses",
                "platform": "MongoDB",
                "url": "https://university.mongodb.com/",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["MongoDB"],
                "description": "Free MongoDB courses from basics to advanced. Get certified.",
            },
            {
                "title": "Java Programming Masterclass",
                "platform": "Udemy",
                "url": "https://www.udemy.com/course/java-the-complete-java-developer-course/",
                "cost": LearningResource.CostChoices.PAID,
                "skills": ["Java"],
                "description": "Complete Java course covering everything from basics to advanced topics.",
            },
            {
                "title": "Data Analysis with Python",
                "platform": "freeCodeCamp",
                "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["Python", "Data Analysis"],
                "description": "Free certification course. Learn data analysis using Python libraries.",
            },
            {
                "title": "PostgreSQL Tutorial",
                "platform": "PostgreSQL Tutorial",
                "url": "https://www.postgresqltutorial.com/",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["PostgreSQL", "SQL"],
                "description": "Comprehensive PostgreSQL tutorial with examples and exercises.",
            },
            {
                "title": "Ruby on Rails Tutorial",
                "platform": "Rails Guides",
                "url": "https://guides.rubyonrails.org/getting_started.html",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["Ruby", "Rails"],
                "description": "Official Rails getting started guide. Learn Ruby on Rails from the basics.",
            },
            {
                "title": "GraphQL Tutorial",
                "platform": "GraphQL",
                "url": "https://graphql.org/learn/",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["GraphQL"],
                "description": "Official GraphQL tutorial. Learn the query language for APIs.",
            },
            {
                "title": "Testing JavaScript Applications",
                "platform": "TestingJavaScript.com",
                "url": "https://testingjavascript.com/",
                "cost": LearningResource.CostChoices.PAID,
                "skills": ["JavaScript", "Testing"],
                "description": "Comprehensive testing course. Learn Jest, React Testing Library, and more.",
            },
            {
                "title": "PHP for Beginners",
                "platform": "PHP.net",
                "url": "https://www.php.net/manual/en/tutorial.php",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["PHP"],
                "description": "Official PHP tutorial. Learn server-side programming with PHP.",
            },
            {
                "title": "Laravel From Scratch",
                "platform": "Laracasts",
                "url": "https://laracasts.com/series/laravel-8-from-scratch",
                "cost": LearningResource.CostChoices.PAID,
                "skills": ["PHP", "Laravel"],
                "description": "Learn Laravel framework step by step. Build real applications.",
            },
            {
                "title": "Machine Learning Crash Course",
                "platform": "Google",
                "url": "https://developers.google.com/machine-learning/crash-course",
                "cost": LearningResource.CostChoices.FREE,
                "skills": ["Python", "Machine Learning"],
                "description": "Google's fast-paced introduction to machine learning with TensorFlow.",
            },
        ]

        created_count = 0
        for resource_data in resources_data:
            # Extract skills from resource data
            skill_names = resource_data.pop("skills")

            # Create resource
            resource, created = LearningResource.objects.get_or_create(
                title=resource_data["title"],
                url=resource_data["url"],
                defaults=resource_data,
            )

            if created:
                # Add skills to resource
                resource_skills = [
                    skills[name] for name in skill_names if name in skills
                ]
                resource.related_skills.set(resource_skills)
                created_count += 1
                self.stdout.write(f"  ✓ Created: {resource.title}")
            else:
                self.stdout.write(f"  ⊙ Exists: {resource.title}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Successfully created {created_count} new resources "
                f"({LearningResource.objects.count()} total resources in database)"
            )
        )
