import django_filters
from .models import LearningResource


class ResourceFilter(django_filters.FilterSet):
    skill = django_filters.CharFilter(method="filter_skill")
    cost = django_filters.CharFilter(field_name="cost", lookup_expr="iexact")
    platform = django_filters.CharFilter(field_name="platform", lookup_expr="icontains")

    class Meta:
        model = LearningResource
        fields = ["skill", "cost", "platform"]

    def filter_skill(self, queryset, name, value):
        return queryset.filter(related_skills__name__icontains=value)
