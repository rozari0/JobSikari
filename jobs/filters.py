import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    skill = django_filters.CharFilter(method="filter_skill")
    location = django_filters.CharFilter(field_name="location", lookup_expr="icontains")
    job_type = django_filters.CharFilter(field_name="job_type", lookup_expr="iexact")

    class Meta:
        model = Job
        fields = ["skill", "location", "job_type", "is_remote"]

    def filter_skill(self, queryset, name, value):
        return queryset.filter(required_skills__name__icontains=value)
