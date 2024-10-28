from django.db import models
from posts.models import Post


class CommentAnalytics(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="analytics")
    date = models.DateField()
    total_comments = models.IntegerField(default=0)
    blocked_comments = models.IntegerField(default=0)

    def __str__(self):
        return f"Analytics for {self.post} on {self.date}"
