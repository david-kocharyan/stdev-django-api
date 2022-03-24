from rest_framework.response import Response
from rest_framework import viewsets, filters, status, generics
from django_filters.rest_framework import DjangoFilterBackend

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer, PostCreateSerializer, PostPartialSerializer, PostByUserIdSerializer


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['title', 'category__name', 'category__slug', 'author__first_name', 'author__last_name']
    ordering_fields = ['title', 'created_at', 'updated_at']
    filter_fields = ['created_at']

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            serializer_class = PostCreateSerializer
        elif self.action == 'update':
            serializer_class = PostPartialSerializer
        else:
            serializer_class = PostSerializer
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        post = serializer.create(validated_data=serializer.validated_data)

        return Response({'result': PostSerializer(post).data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.update(instance=self.get_object(), validated_data=serializer.validated_data)

        return Response({'result': PostSerializer(post).data}, status=status.HTTP_200_OK)


class GetPostsByUserIdView(generics.ListAPIView):
    serializer_class = PostByUserIdSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        return Post.objects.filter(author=self.kwargs.get('pk')).order_by("-pk")
