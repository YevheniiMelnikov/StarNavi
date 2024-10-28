from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Comment
from .serializers import CommentSerializer
from .tasks import send_auto_reply
from posts.models import AutoReply
from posts.serializers import AutoReplySerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(is_blocked=False).order_by("-created_at")

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        if comment.post.auto_reply_enabled and hasattr(comment.post, "auto_reply"):
            send_auto_reply.apply_async(args=[comment.id], countdown=comment.post.reply_delay)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        comment = Comment.objects.get(id=serializer.instance.id)
        if comment.is_blocked:
            return Response(
                {"detail": "Your comment has been blocked because of profanity"},
                status=status.HTTP_403_FORBIDDEN,
                headers=headers,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AutoReplyViewSet(viewsets.ModelViewSet):
    queryset = AutoReply.objects.all()
    serializer_class = AutoReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
