from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.conf import settings

from .models import User


class TokenObtainPairPatchedSerializer(TokenObtainSerializer):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if not user:
            raise serializers.ValidationError({'email': 'There is no user with this credentials'})

        if not user.password:
            raise serializers.ValidationError({'password': 'Please verify user and set password'})

        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return data


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'image',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def get_image(self, obj):
        return f"{settings.BASE_URL}/media/{obj.image}"


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate_password(self, value):
        """Validates that a password is as least 8 characters long and has at least
            2 digits and 1 Upper case letter.
            """
        value = str(value)
        # check for len
        if len(value) < 6:
            raise serializers.ValidationError('Password must be at least 6 characters long')

        # check for 2 digits
        if sum(c.isdigit() for c in value) < 2:
            raise serializers.ValidationError('Password must container at least 2 digits')

        # check for uppercase letter
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError('Password must container at least 1 uppercase letter')

        return value

    def create(self, validated_data):
        User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            image=validated_data['image'],
            password=make_password(validated_data['password']),
            is_active=True
        )
