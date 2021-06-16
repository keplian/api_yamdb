from rest_framework import viewsets
from .models import Titles
from .serializers import TitlesSerializer
from .pagination import StandardResultsSetPagination
from .filters import TitlesFilter
from django_filters.rest_framework import DjangoFilterBackend


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
