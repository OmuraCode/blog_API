from rest_framework import generics, permissions
from .models import Post
from . import serializers


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PostListSerializer
        return serializers.PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



