from rest_framework import pagination, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Category, Comment, Genre, Review, Title, User




class UserSerializer(serializers.ModelSerializer):
    lookup_field = "username"

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "username",
            "bio",
            "email",
            "role",
        )
        model = User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    class Meta:
        fields = ("id", "author", "text", "pub_date")
        model = Comment


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    # genre = GenreSerializer()
    # category = CategorySerializer()
    # genre = serializers.SlugRelatedField(
    #     many=True,
    #     queryset=Genre.objects.all(),
    #     read_only=True,
    #     slug_field='name'
    # )
    # gen = GenreSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title
        read_only_fields = ('rating',)
        # depth = 1
        
    # def get_genre(self, obj):
    #     if Genre.objects.filter(id=obj.id):
    #         genre = {
    #             'name': Genre.objects.get(id=obj.id).name,
    #             'slug': Genre.objects.get(id=obj.id).slug
    #         }
    #     else:
    #         genre = None
    #     return genre

    # def get_category(self, obj):
    #     if Category.objects.filter(id=obj.id):
    #         category = {
    #             'name': Category.objects.get(id=obj.id).name,
    #             'slug': Category.objects.get(id=obj.id).slug
    #         }
    #     else:
    #         category = None
    #     return category

    def get_rating(self, obj):
        if Review.objects.filter(id=obj.id):
            rating = Review.objects.get(id=obj.id).score
        else:
            rating = None
        return rating


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["password"]
        del self.fields["username"]
        self.fields["confirmation_code"] = serializers.CharField(required=True)
        self.fields["email"] = serializers.EmailField(required=True)

    def validate(self, attrs):
        data = {}
        user = User.objects.get(email=attrs["email"])
        confirmation_code = User.objects.get(
            confirmation_code=attrs["confirmation_code"]
        )
        refresh = self.get_token(user)
        if user and confirmation_code:
            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)
            user.confirmation_code = ""
            user.save()
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
