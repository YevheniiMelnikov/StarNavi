import loguru
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer


logger = loguru.logger


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.objects.filter(is_blocked=False).order_by("-created_at")

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        if post.auto_reply_enabled and hasattr(post, "auto_reply"):
            logger.info(f"Auto reply enabled for post ID {post.id}")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        post = Post.objects.get(id=serializer.instance.id)
        if post.is_blocked:
            return Response(
                {"detail": "Your post has been blocked because of profanity"},
                status=status.HTTP_403_FORBIDDEN,
                headers=headers,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
