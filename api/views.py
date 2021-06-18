from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework import filters
from rest_framework.response import Response

from .filters import TitleFilter
from .models import Comment, Review, Title
from .models import Category
from .paginations import StandardResultsSetPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer, TitleSerializer
from .serializers import CategorySerializer



class TitleModelViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    # def perform_create(self, serializer):
    #     serializer.save(
    #         name=self.request.query_params['name'],
    #         genre__slug=self.request.query_params['genre'],
    #         category__slug=self.request.query_params['category'],
    #     ) НЕ РАБОТАЕТ


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data['name'],
            slug=self.request.data['slug']
        )   


class ReviewModelViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        get_object_or_404(Title, pk=self.request.data['title_id'])
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Review.objects.filter(id=self.kwargs['id'])


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        get_object_or_404(Review, pk=self.request.data['review_id'])
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.kwargs['review_id'])

#
# class TitleModelViewSet(viewsets.ModelViewSet):
#     queryset = Title.objects.all()
#     serializer_class = TitleSerializer
#     permission_classes = [IsAuthorOrReadOnly,
#                           permissions.IsAuthenticatedOrReadOnly]
#
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = TitleFilter
#
#     def perform_create(self, serializer):
#         user = User.objects.filter(username=self.request.user)
#         if not user.exists():
#             return Response(serializer.errors,
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         serializer.save(author=self.request.user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def get_queryset(self):
#         group_id = self.request.query_params.get('group', None)
#         if group_id is not None:
#             return self.queryset.filter(group=group_id)
