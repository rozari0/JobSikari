from ninja import Schema


class JobSchema(Schema):
    id: int
    title: str
    company: str
    location: str | None = None
    is_remote: bool
    required_skills: list[str] | None = None
    recommended_experience: str | None = None
    job_type: str
    description: str | None = None
    posted_at: str


class CreateJobSchema(Schema):
    title: str
    company: str
    location: str | None = None
    is_remote: bool | None = False
    required_skills: list[str] | None = None
    recommended_experience: str | None = None
    job_type: str | None = None
    description: str | None = None


class JobMatchSchema(Schema):
    """Schema for matched job with score and matching skills."""

    job_id: int
    title: str
    company: str
    match_score: float
    matching_skills: list[str]
    total_skills: int


class JobRecommendationSchema(Schema):
    """Schema for job recommendation response with full job details."""

    job: JobSchema
    match_score: float
    matching_skills: list[str]
