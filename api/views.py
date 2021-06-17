from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from .paginations import StandardResultsSetPagination


from .filters import TitleFilter
from .models import Review, Title, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import ReviewSerializer, TitleSerializer, CommentSerializer


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


class TitleModelViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

