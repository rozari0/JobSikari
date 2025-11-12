"""
Management command to seed all data (jobs and resources) at once.

Usage:
    python manage.py seed_all
    python manage.py seed_all --clear  # Clear existing data first
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed all data: jobs and resources"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing data before seeding",
        )

    def handle(self, *args, **options):
        clear_flag = options["clear"]

        self.stdout.write(self.style.WARNING("=" * 60))
        self.stdout.write(self.style.WARNING("Starting database seeding..."))
        self.stdout.write(self.style.WARNING("=" * 60))

        # Seed jobs
        self.stdout.write("\n" + self.style.HTTP_INFO("SEEDING JOBS"))
        self.stdout.write("-" * 60)
        call_command("seed_jobs", clear=clear_flag)

        # Seed resources
        self.stdout.write("\n" + self.style.HTTP_INFO("SEEDING LEARNING RESOURCES"))
        self.stdout.write("-" * 60)
        call_command("seed_resources", clear=clear_flag)

        self.stdout.write("\n" + self.style.WARNING("=" * 60))
        self.stdout.write(
            self.style.SUCCESS("✓ Database seeding completed successfully!")
        )
        self.stdout.write(self.style.WARNING("=" * 60))
