from better_profanity import profanity
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from posts.models import Post

User = get_user_model()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(default=timezone.now)
    is_blocked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if profanity.contains_profanity(self.content):
            self.is_blocked = True
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
