from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from .filters import TitleFilter
from .models import Comment, Review, Title, User
from .paginations import StandardResultsSetPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
)


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination


class TitleModelViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        user = User.objects.filter(username=self.request.user)
        if not user.exists():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def get_queryset(self):
    #     group_id = self.request.query_params.get('id', None)
    #     if group_id is not None:
    #         return self.queryset.filter(group=group_id)


class ReviewModelViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    ]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        get_object_or_404(Title, pk=self.request.data["title_id"])

        user = User.objects.get(username="bob")
        print(user.__dict__)

        if user is None:
            print(f"UUUUUWEEEE:::::::::::: {user}")
            raise ParseError("Bad Request")
            # return Response(serializer.errors,
            #                 status=status.HTTP_400_BAD_REQUEST)

        # serializer.save(author=self.request.user)

        serializer.save(author=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Review.objects.filter(id=self.kwargs["id"])


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    ]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        get_object_or_404(Review, pk=self.request.data["review_id"])
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.kwargs["review_id"])


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
