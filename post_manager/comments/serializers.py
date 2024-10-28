from rest_framework import serializers
from .models import Comment
from posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["id", "author", "created_at", "is_blocked"]
