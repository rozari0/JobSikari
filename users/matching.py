"""
Matching logic for JobSikari - skill-based recommendations.

This module provides non-AI matching algorithms that calculate
job and resource recommendations based on user profile skills.
"""

from typing import TypedDict


class JobMatch(TypedDict):
    """Type for job matching results."""

    job_id: int
    title: str
    company: str
    match_score: float
    matching_skills: list[str]
    total_skills: int


class ResourceMatch(TypedDict):
    """Type for resource matching results."""

    resource_id: int
    title: str
    platform: str
    match_score: float
    matching_skills: list[str]
    total_skills: int


def calculate_skill_overlap(user_skills: set[str], required_skills: set[str]) -> float:
    """
    Calculate skill overlap percentage between user and required skills.

    Args:
        user_skills: Set of skill names from user profile
        required_skills: Set of skill names required by job/resource

    Returns:
        Float between 0.0 and 1.0 representing match percentage
    """
    if not required_skills:
        # If no skills required, consider it a 50% baseline match
        return 0.5

    if not user_skills:
        # User has no skills
        return 0.0

    matching = user_skills.intersection(required_skills)
    overlap = len(matching) / len(required_skills)
    return overlap


def match_jobs_for_user(user_profile, jobs_queryset, limit: int = 10) -> list[JobMatch]:
    """
    Find and rank jobs based on skill overlap with user profile.

    Args:
        user_profile: UserProfile instance
        jobs_queryset: QuerySet of Job objects to match against
        limit: Maximum number of results to return

    Returns:
        List of JobMatch dictionaries sorted by match_score (descending)
    """
    user_skill_names = set(skill.name.lower() for skill in user_profile.skills.all())

    matches = []
    for job in jobs_queryset:
        job_skill_names = set(skill.name.lower() for skill in job.required_skills.all())

        match_score = calculate_skill_overlap(user_skill_names, job_skill_names)

        # Get the actual matching skill names (case-sensitive originals)
        matching_skills = [
            skill.name
            for skill in job.required_skills.all()
            if skill.name.lower() in user_skill_names
        ]

        matches.append(
            {
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "match_score": match_score,
                "matching_skills": matching_skills,
                "total_skills": len(job_skill_names),
            }
        )

    # Sort by match_score descending, then by number of matching skills
    matches.sort(
        key=lambda x: (x["match_score"], len(x["matching_skills"])), reverse=True
    )

    return matches[:limit]


def match_resources_for_user(
    user_profile, resources_queryset, limit: int = 10
) -> list[ResourceMatch]:
    """
    Find and rank learning resources based on skill overlap with user profile.

    Args:
        user_profile: UserProfile instance
        resources_queryset: QuerySet of LearningResource objects to match against
        limit: Maximum number of results to return

    Returns:
        List of ResourceMatch dictionaries sorted by match_score (descending)
    """
    user_skill_names = set(skill.name.lower() for skill in user_profile.skills.all())

    matches = []
    for resource in resources_queryset:
        resource_skill_names = set(
            skill.name.lower() for skill in resource.related_skills.all()
        )

        match_score = calculate_skill_overlap(user_skill_names, resource_skill_names)

        # Get the actual matching skill names (case-sensitive originals)
        matching_skills = [
            skill.name
            for skill in resource.related_skills.all()
            if skill.name.lower() in user_skill_names
        ]

        matches.append(
            {
                "resource_id": resource.id,
                "title": resource.title,
                "platform": resource.platform or "",
                "match_score": match_score,
                "matching_skills": matching_skills,
                "total_skills": len(resource_skill_names),
            }
        )

    # Sort by match_score descending, then by number of matching skills
    matches.sort(
        key=lambda x: (x["match_score"], len(x["matching_skills"])), reverse=True
    )

    return matches[:limit]
