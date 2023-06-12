from rest_framework import serializers

from category.models import Category
from .models import Post


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'category', 'preview')


class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True,
                                                  queryset=Category.objects.all())
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Post
        fields = '__all__'



