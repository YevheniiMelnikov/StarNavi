from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post
from better_profanity import profanity

User = get_user_model()


class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.post_url = reverse("post-list")

    def test_create_post_clean_content(self):
        self.client.login(username="testuser", password="testpassword")
        data = {
            "title": "Тестовый пост",
            "content": "Это содержимое тестового поста.",
            "auto_reply_enabled": False,
            "reply_delay": 60,
        }
        response = self.client.post(self.post_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=response.data["id"])
        self.assertFalse(post.is_blocked)

    def test_create_post_profanity_content(self):
        self.client.login(username="testuser", password="testpassword")
        data = {
            "title": "Blocked post",
            "content": "Some bad content",
            "auto_reply_enabled": False,
            "reply_delay": 60,
        }
        profanity.add_censor_words(["bad"])
        response = self.client.post(self.post_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        try:
            post = Post.objects.get(title="Blocked post")
        except Post.DoesNotExist:
            self.fail("Post was not created despite profanity in content.")

        self.assertTrue(post.is_blocked)
