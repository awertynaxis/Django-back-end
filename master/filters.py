from django_filters import rest_framework as filters
from master.models import Service


class SkillsFilter(filters.FilterSet):
    master_id = filters.CharFilter(field_name="master__id", lookup_expr='exact')

    class Meta:
        model = Service
        fields = ['master_id']


class DetailSkillFilter(filters.FilterSet):
    service = filters.NumberFilter(field_name="id", lookup_expr='exact')

    class Meta:
        model = Service
        fields = ['service']
