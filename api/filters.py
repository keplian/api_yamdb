import django_filters
from django_filters.rest_framework import filters

from .models import Title


class TitleFilter(django_filters.FilterSet):
    year = filters.NumberFilter(field_name='year', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='exact'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='exact'
    )

    class Meta:
        model = Title
        fields = ['year', 'name', 'category', 'genre']
