from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post
from .models import Comment
from better_profanity import profanity

User = get_user_model()


class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.post = Post.objects.create(title="Test post", content="Test string", author=self.user)
        self.comment_url = reverse("comment-list")

    def test_create_comment_clean_content(self):
        self.client.login(username="testuser", password="testpassword")
        data = {"post": self.post.id, "content": "This comment is fine"}
        response = self.client.post(self.comment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.get(id=response.data["id"])
        self.assertFalse(comment.is_blocked)

    def test_create_comment_profanity_content(self):
        self.client.login(username="testuser", password="testpassword")
        data = {"post": self.post.id, "content": "This is a bad comment"}
        profanity.add_censor_words(["bad"])

        response = self.client.post(self.comment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        comment = Comment.objects.get(content="This is a bad comment")
        self.assertTrue(comment.is_blocked)
