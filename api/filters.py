import django_filters
from django_filters.rest_framework import filters

from .models import Title


class TitleFilter(django_filters.FilterSet):
    year = filters.NumberFilter(field_name='year', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['year', 'name']