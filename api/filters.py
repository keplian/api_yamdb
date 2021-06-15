from django_filters import rest_framework as filters

from .models import Title


class TitleFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='year',
                                   lookup_expr='gte')
    date_to = filters.DateFilter(field_name='year',
                                 lookup_expr='lte')

    class Meta:
        model = Title
        fields = ['date_from', 'date_to']
