from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
<<<<<<< HEAD
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title, User
from .paginations import StandardResultsSetPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer)
=======
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .filters import TitleFilter
from .models import Category, Comment, Review, Title, User, Genre
from .paginations import StandardResultsSetPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          ReviewSerializer, TitleSerializer, UserSerializer,
                          GenreSerializer)
>>>>>>> 80a9ef9ea70f1e3b2259f7a49703dad7ebf9d412


class UserModelViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
<<<<<<< HEAD
=======
    permission_classes = [permissions.IsAuthenticated]

    @action(
        methods=["PATCH", "GET"],
        permission_classes=[permissions.IsAuthenticated],
        detail=False,
        url_path="me",
    )
    def user_me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
>>>>>>> 80a9ef9ea70f1e3b2259f7a49703dad7ebf9d412


class TitleModelViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def perform_create(self, serializer):
<<<<<<< HEAD
        genre = get_object_or_404(Genre, slug=self.request.data['genre'])
        category = get_object_or_404(Category, slug=self.request.data['category'])
        serializer.save(
            genre_id=genre.id,
            category_id=category.id,
        )
=======
        user = User.objects.filter(username=self.request.user)
        if not user.exists():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        category_id = self.request.query_params.get('group', None)
        if category_id is not None:
            #  через ORM отфильтровать объекты модели User
            #  по значению параметра username, полученнго в запросе
            return self.queryset.filter(category=category_id)
    # def get_queryset(self):
    #     group_id = self.request.query_params.get('id', None)
    #     if group_id is not None:
    #         return self.queryset.filter(group=group_id)

    # def perform_create(self, serializer):
    #     serializer.save(
    #         name=self.request.query_params['name'],
    #         genre__slug=self.request.query_params['genre'],
    #         category__slug=self.request.query_params['category'],
    #     ) НЕ РАБОТАЕТ

>>>>>>> 80a9ef9ea70f1e3b2259f7a49703dad7ebf9d412

class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data['name'],
            slug=self.request.data['slug']
        )

<<<<<<< HEAD
    def perform_destroy(self, serializer):
        serializer = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        serializer.delete()

=======
>>>>>>> 80a9ef9ea70f1e3b2259f7a49703dad7ebf9d412

class GenreModelViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
<<<<<<< HEAD
    # lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
=======
>>>>>>> 80a9ef9ea70f1e3b2259f7a49703dad7ebf9d412

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data['name'],
            slug=self.request.data['slug']
        )
<<<<<<< HEAD

    def perform_destroy(self, serializer):
        serializer = get_object_or_404(Genre, slug=self.kwargs.get('slug'))
        serializer.delete()
=======
>>>>>>> 80a9ef9ea70f1e3b2259f7a49703dad7ebf9d412


class ReviewModelViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    ]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.request.data["title_id"])
        user = User.objects.get(username=self.request.user)
        if user is None:
            raise ParseError("Bad Request")

        serializer.save(author=user, title=title)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Review.objects.filter(title_id=self.kwargs["id"])


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    ]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        review =get_object_or_404(Review, pk=self.request.data["review_id"])
        title =get_object_or_404(Title, pk=self.request.data["title_id"])
        serializer.save(author=self.request.user, review=review, title=title)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.kwargs["review_id"])


@api_view(["POST"])
def email_auth(request):
    user = get_object_or_404(User, email=request.data["email"])
    confirmation_code = get_random_string()
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        subject="Confirmation code for token from YAMDB",
        message=str(confirmation_code),
        from_email=["admin@gmail.com"],
        recipient_list=[request.data["email"]],
    )
    return Response(data="Email was sent", status=status.HTTP_201_CREATED)
