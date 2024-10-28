from better_profanity import profanity
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auto_reply_enabled = models.BooleanField(default=False)
    reply_delay = models.IntegerField(default=60)
    is_blocked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if profanity.contains_profanity(self.content):
            self.is_blocked = True
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class AutoReply(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="auto_reply")

    def __str__(self):
        return f"AutoReply for Post: {self.post.title}"
