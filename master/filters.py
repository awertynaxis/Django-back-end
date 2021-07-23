from django_filters import rest_framework as filters
from master.models import Service


class SkillsFilter(filters.FilterSet):
    nickname = filters.CharFilter(field_name="master__nickname", lookup_expr='exact')

    class Meta:
        model = Service
        fields = ['nickname']


class DetailSkillFilter(filters.FilterSet):
    service = filters.NumberFilter(field_name="id", lookup_expr='exact')

    class Meta:
        model = Service
        fields = ['service']