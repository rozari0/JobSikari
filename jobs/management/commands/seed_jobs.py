"""
Management command to seed the database with entry-level job postings.

Usage:
    python manage.py seed_jobs
    python manage.py seed_jobs --clear  # Clear existing jobs first
"""

from django.core.management.base import BaseCommand

from jobs.models import Job
from users.models import Skill


class Command(BaseCommand):
    help = "Seed the database with entry-level job postings"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing jobs before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing jobs...")
            Job.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("✓ Cleared all jobs"))

        self.stdout.write("Creating skills...")
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
        ]

        skills = {}
        for skill_name in skills_data:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            skills[skill_name] = skill

        self.stdout.write(
            self.style.SUCCESS(f"✓ Created/verified {len(skills)} skills")
        )

        self.stdout.write("Seeding jobs...")

        jobs_data = [
            {
                "title": "Junior Python Developer",
                "company": "TechStart Solutions",
                "location": "Dhaka",
                "is_remote": False,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["Python", "Django", "SQL", "Git"],
                "description": "We're looking for a Junior Python Developer to join our growing team. You'll work on backend services using Django and contribute to our API development.",
            },
            {
                "title": "Frontend Developer Intern",
                "company": "WebCraft Studios",
                "location": "Remote",
                "is_remote": True,
                "job_type": Job.JobType.INTERNSHIP,
                "recommended_experience": "Intern",
                "skills": ["JavaScript", "React", "HTML", "CSS"],
                "description": "Exciting opportunity for a frontend development intern. Work with modern React applications and learn from experienced developers.",
            },
            {
                "title": "Entry Level Full Stack Developer",
                "company": "CodeLabs Inc",
                "location": "Chittagong",
                "is_remote": False,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["JavaScript", "Node.js", "React", "MongoDB", "Git"],
                "description": "Join our team as a full stack developer. Work on exciting projects using the MERN stack. Great mentorship and learning opportunities.",
            },
            {
                "title": "Junior Backend Engineer",
                "company": "DataFlow Systems",
                "location": "Remote",
                "is_remote": True,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                "description": "Looking for a backend engineer to help build scalable APIs. Experience with Python and modern frameworks preferred.",
            },
            {
                "title": "Web Development Intern",
                "company": "StartupHub",
                "location": "Remote",
                "is_remote": True,
                "job_type": Job.JobType.INTERNSHIP,
                "recommended_experience": "Intern",
                "skills": ["HTML", "CSS", "JavaScript", "Git"],
                "description": "Summer internship program for aspiring web developers. Learn modern web development practices and build real projects.",
            },
            {
                "title": "Junior Software Engineer",
                "company": "TechVentures LLC",
                "location": "Dhaka",
                "is_remote": False,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["Java", "Spring Boot", "SQL", "Git"],
                "description": "Entry-level position for software engineers. Work on enterprise applications using Java and Spring framework.",
            },
            {
                "title": "React Developer - Entry Level",
                "company": "Frontend Masters Co",
                "location": "Remote",
                "is_remote": True,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["React", "JavaScript", "TypeScript", "CSS"],
                "description": "Build modern web applications with React. We're looking for passionate developers eager to learn and grow.",
            },
            {
                "title": "Data Analyst Intern",
                "company": "Analytics Pro",
                "location": "Dhaka",
                "is_remote": False,
                "job_type": Job.JobType.INTERNSHIP,
                "recommended_experience": "Intern",
                "skills": ["Python", "Data Analysis", "Excel", "SQL"],
                "description": "Internship opportunity in data analytics. Work with real datasets and create insightful visualizations.",
            },
            {
                "title": "Junior DevOps Engineer",
                "company": "CloudTech Solutions",
                "location": "Remote",
                "is_remote": True,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["Docker", "Git", "AWS", "Python"],
                "description": "Learn DevOps practices while helping maintain our cloud infrastructure. Great opportunity for growth.",
            },
            {
                "title": "PHP Developer - Junior",
                "company": "WebSolutions Inc",
                "location": "Sylhet",
                "is_remote": False,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["PHP", "Laravel", "MySQL", "Git"],
                "description": "Join our team to work on web applications using PHP and Laravel. Supportive environment for learning.",
            },
            {
                "title": "Part-Time Frontend Developer",
                "company": "Freelance Hub",
                "location": "Remote",
                "is_remote": True,
                "job_type": Job.JobType.PART_TIME,
                "recommended_experience": "Junior",
                "skills": ["HTML", "CSS", "JavaScript", "Vue.js"],
                "description": "Flexible part-time role building user interfaces. Perfect for students or those seeking flexible hours.",
            },
            {
                "title": "Junior Full Stack Engineer",
                "company": "Innovation Labs",
                "location": "Remote",
                "is_remote": True,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["Python", "Django", "React", "PostgreSQL"],
                "description": "Work on full stack applications with modern technologies. Collaborative team environment.",
            },
            {
                "title": "Mobile App Development Intern",
                "company": "AppCreators",
                "location": "Dhaka",
                "is_remote": False,
                "job_type": Job.JobType.INTERNSHIP,
                "recommended_experience": "Intern",
                "skills": ["JavaScript", "React", "Node.js", "Git"],
                "description": "Summer internship developing mobile applications using React Native. Learn from experienced developers.",
            },
            {
                "title": "Junior .NET Developer",
                "company": "Enterprise Solutions Corp",
                "location": "Chittagong",
                "is_remote": False,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["C#", ".NET", "SQL", "Azure"],
                "description": "Entry-level position working with .NET framework. Build enterprise applications for Fortune 500 clients.",
            },
            {
                "title": "API Developer - Entry Level",
                "company": "API Masters",
                "location": "Remote",
                "is_remote": True,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["Python", "FastAPI", "REST API", "Testing"],
                "description": "Design and build RESTful APIs. Learn API best practices and work with modern Python frameworks.",
            },
            {
                "title": "JavaScript Developer",
                "company": "WebTech Solutions",
                "location": "Remote",
                "is_remote": True,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["JavaScript", "TypeScript", "Node.js", "Git"],
                "description": "Join our JavaScript team. Work on both frontend and backend using modern JS technologies.",
            },
            {
                "title": "Ruby on Rails Developer",
                "company": "RailsExperts",
                "location": "Remote",
                "is_remote": True,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["Ruby", "Rails", "PostgreSQL", "Git"],
                "description": "Build web applications with Ruby on Rails. Great opportunity to learn from Rails experts.",
            },
            {
                "title": "UI/UX Developer Intern",
                "company": "Design Studio",
                "location": "Dhaka",
                "is_remote": False,
                "job_type": Job.JobType.INTERNSHIP,
                "recommended_experience": "Intern",
                "skills": ["HTML", "CSS", "JavaScript", "Tailwind CSS"],
                "description": "Internship focused on frontend development and design. Create beautiful user interfaces.",
            },
            {
                "title": "Junior Backend Developer",
                "company": "ServerTech Inc",
                "location": "Remote",
                "is_remote": True,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Junior",
                "skills": ["Node.js", "MongoDB", "REST API", "Docker"],
                "description": "Backend development role working with Node.js and MongoDB. Build scalable server applications.",
            },
            {
                "title": "Software Engineer Trainee",
                "company": "TechAcademy Corp",
                "location": "Dhaka",
                "is_remote": False,
                "job_type": Job.JobType.FULL_TIME,
                "recommended_experience": "Intern",
                "skills": ["Python", "JavaScript", "SQL", "Git"],
                "description": "Training program for new software engineers. Learn best practices while working on real projects.",
            },
        ]

        created_count = 0
        for job_data in jobs_data:
            # Extract skills from job data
            skill_names = job_data.pop("skills")

            # Create job
            job, created = Job.objects.get_or_create(
                title=job_data["title"], company=job_data["company"], defaults=job_data
            )

            if created:
                # Add skills to job
                job_skills = [skills[name] for name in skill_names if name in skills]
                job.required_skills.set(job_skills)
                created_count += 1
                self.stdout.write(f"  ✓ Created: {job.title} at {job.company}")
            else:
                self.stdout.write(f"  ⊙ Exists: {job.title} at {job.company}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Successfully created {created_count} new jobs "
                f"({Job.objects.count()} total jobs in database)"
            )
        )
