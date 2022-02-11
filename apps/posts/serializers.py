from rest_framework import serializers
from django.conf import settings

from apps.posts.models import Post
from apps.users.models import User
from apps.categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'slug',
        )


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'full_name'
        )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=125)
    description = serializers.CharField(required=True, max_length=500)
    image = serializers.SerializerMethodField()
    category = CategorySerializer(required=True)
    author = UserSerializer(required=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'description',
            'image',
            'category',
            'author',
        )
        depth = 1

    def get_image(self, obj):
        return f"{settings.BASE_URL}/media/{obj.image}"


class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=125)
    description = serializers.CharField(required=True, max_length=250)
    image = serializers.ImageField(required=True)
    category = serializers.IntegerField(required=True)

    def create(self, validated_data):
        category = Category.objects.filter(pk=validated_data['category']).first()
        post = Post.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            image=validated_data['image'],
            category=category,
            author=self.context.get("user"),
        )
        return post


class PostPartialSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, max_length=125)
    description = serializers.CharField(required=False, max_length=250)
    image = serializers.ImageField(allow_null=True)
    category = serializers.IntegerField(required=True)

    def update(self, instance, validated_data):
        category = Category.objects.get(pk=validated_data['category'])
        if validated_data['image']:
            instance.image = validated_data['image']

        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.category = category
        instance.save()

        return instance


class PostByUserIdSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = CategorySerializer(required=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'description',
            'image',
            'category',
        )

    def get_image(self, obj):
        return f"{settings.BASE_URL}/media/{obj.image}"
