from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from comment.serializers import CommentSerializer
from like.models import Favorite
from like.serializers import LikeSerializer, LikeUserSerializer
from .models import Post
from . import serializers
from .permissions import IsAuthor, IsAuthorOrAdmin


class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('owner', 'category')
    search_fields = ('title', 'body')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        return serializers.PostDetailSerializer

    def get_permissions(self):
        # удалять может только автор поста и админы
        if self.action == 'destroy':
            return (IsAuthorOrAdmin(),)
        # обновлять может только автор поста
        elif self.action in ('update', 'partial_update'):
            return (IsAuthor(),)
        # просматривать могкт все
        # но создавать может залогиненный пользователь
        return (permissions.IsAuthenticatedOrReadOnly(),)

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        print(post, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        comments = post.comments.all()
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(serializer.data, status=200)

    @action(['GET'], detail=True)
    def likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikeUserSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def favorites(self, request, pk):
        post = self.get_object()  # Post.objects.get(id=pk)
        user = request.user
        favorite = user.favorites.filter(post=post)

        if request.method == 'POST':
            if user.favorites.filter(post=post).exists():
                return Response({'msg': 'Already in favorites'}, status=400)
            Favorite.objects.create(owner=user, post=post)
            return Response({'msg': 'Added to Favorites'}, status=201)

        if favorite.exists():
            favorite.delete()
            return Response({'msg': 'Deleted from Favorites'}, status=204)
        return Response({'msg': 'Post not found in favorites'}, status=404)

# generics
# class PostListCreateView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return serializers.PostListSerializer
#         return serializers.PostCreateSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return serializers.PostCreateSerializer
#         return serializers.PostDetailSerializer
#
#     def get_permissions(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return [IsAuthor()]
#         elif self.request.method == 'DELETE':
#             return [IsAuthorOrAdmin()]
#         return [permissions.AllowAny()]
