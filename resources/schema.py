from ninja import Schema


class LearningResourceSchema(Schema):
    id: int
    title: str
    platform: str | None = None
    url: str
    related_skills: list[str] | None = None
    cost: str
    description: str | None = None


class CreateLearningResourceSchema(Schema):
    title: str
    platform: str | None = None
    url: str
    related_skills: list[str] | None = None
    cost: str | None = None
    description: str | None = None


class ResourceMatchSchema(Schema):
    """Schema for matched resource with score and matching skills."""

    resource_id: int
    title: str
    platform: str
    match_score: float
    matching_skills: list[str]
    total_skills: int


class ResourceRecommendationSchema(Schema):
    """Schema for resource recommendation response with full details."""

    resource: LearningResourceSchema
    match_score: float
    matching_skills: list[str]
