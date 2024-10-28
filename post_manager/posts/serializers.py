from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, AutoReply

User = get_user_model()


class AutoReplySerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = AutoReply
        fields = "__all__"
        read_only_fields = ["id"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    auto_reply = AutoReplySerializer(required=False)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["id", "author", "created_at", "updated_at", "is_blocked"]
