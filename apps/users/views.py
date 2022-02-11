import logging
from django.db import transaction
from rest_framework import viewsets, views, generics, status, mixins, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import (OutstandingToken, BlacklistedToken)

from apps.posts.models import Post
from apps.users.models import User
from apps.users.serializers import (TokenObtainPairPatchedSerializer, UserRegistrationSerializer, UserSerializer)

logger = logging.getLogger(__name__)


class UserRegisterView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response({'message': 'Thank you! Now you can sign in'}, status=status.HTTP_200_OK, )


class TokenObtainPairPatchedView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairPatchedSerializer


class UserLogoutView(views.APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': "User lodged out successfully."}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as err:
            logger.debug(err)
            return Response({'message': 'Something went wrong, please try again.'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAllView(views.APIView):
    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)

            return Response({'message': "User lodged out successfully from all devices."},
                            status=status.HTTP_205_RESET_CONTENT)

        except Exception as err:
            logger.debug(err)
            return Response({'message': 'Something went wrong, please try again.'},
                            status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserByIdView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
