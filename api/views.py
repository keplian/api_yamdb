from functools import partial

from api_yamdb.settings import ROLES_PERMISSIONS
from django.core.mail import send_mail
from .mixin import CreateListDestroyModelMixinViewSet
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title, User
from .paginations import StandardResultsSetPagination
from .permissions import IsAuthorOrReadOnly, PermissonForRole
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
)


class UserModelViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [
        permissions.IsAuthenticated,
        partial(PermissonForRole, ROLES_PERMISSIONS.get("Users")),
    ]

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


class TitleModelViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [
        partial(PermissonForRole, ROLES_PERMISSIONS.get("Categories")),
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    # def retrieve(self, request, pk=None):
    #     title = get_object_or_404(self.queryset, pk=pk)
    #     serializers = TitleSerializer(title)
    #     return Response(serializers.data)

    def perform_create(self, serializer):
        a = self.request.data['genre']
        c = [x.strip() for x in a.split(',')]
        genre = Genre.objects.none()
        for i in c:
            genre_a = Genre.objects.filter(slug=i)
            genre = genre.union(genre_a)
        
        category = get_object_or_404(
            Category,
            slug=self.request.data['category']
        )
        serializer.save(
            genre=genre,
            category_id=category.id,
        )

    def perform_update(self, serializer):
        if 'genre' in self.request.data:
            a = self.request.data['genre']
            c = [x.strip() for x in a.split(',')]
            genre = Genre.objects.none()
            for i in c:
                genre_a = Genre.objects.filter(slug=i)
                genre = genre.union(genre_a)
            genre_title = self.get_object().genre.all()
            genre = genre_title.union(genre)
        else:
            # slug = self.request.POST['genre']
            genre = self.get_object().genre.all()
        if 'category' in self.request.data:
            category = get_object_or_404(
                Category,
                slug=self.request.data['category']
            )
        else:
            slug = self.get_object().category.slug
            category = get_object_or_404(Category, slug=slug)
        serializer.save(
            genre=genre,
            category_id=category.id,
        )

# <<<<<<< HEAD
#     def get_queryset(self):
#         category_id = self.request.query_params.get("group", None)
#         if category_id is not None:
#             #  через ORM отфильтровать объекты модели User
#             #  по значению параметра username, полученнго в запросе
#             return self.queryset.filter(category=category_id)
#
#     # def get_queryset(self):
#     #     group_id = self.request.query_params.get('id', None)
#     #     if group_id is not None:
#     #         return self.queryset.filter(group=group_id)
#
#     # def perform_create(self, serializer):
#     #     serializer.save(
#     #         name=self.request.query_params['name'],
#     #         genre__slug=self.request.query_params['genre'],
#     #         category__slug=self.request.query_params['category'],
#     #     ) НЕ РАБОТАЕТ
# =======
#
#
# >>>>>>> 261447e1b5e86dd45959261b9428ea4a159a07ab


class CategoryModelViewSet(CreateListDestroyModelMixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [
        partial(PermissonForRole, ROLES_PERMISSIONS.get("Categories")),
        IsAuthenticatedOrReadOnly,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data["name"], slug=self.request.data["slug"]
        )

    def perform_destroy(self, serializer):
        serializer = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        serializer.delete()

    # def get_queryset(self):
    #     slug = self.request.query_params.get('slug', None)
    #     if slug is not None:
    #         return self.queryset.filter(group=group_id)

class GenreModelViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        partial(PermissonForRole, ROLES_PERMISSIONS.get("Categories")),
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]

    search_fields = ['name', ]
    # lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def perform_create(self, serializer):
        serializer.save(
            name=self.request.data["name"], slug=self.request.data["slug"]
        )

    def perform_destroy(self, serializer):
        serializer = get_object_or_404(Genre, slug=self.kwargs.get('slug'))
        serializer.delete()


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
        review = get_object_or_404(Review, pk=self.request.data["review_id"])
        title = get_object_or_404(Title, pk=self.request.data["title_id"])
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
