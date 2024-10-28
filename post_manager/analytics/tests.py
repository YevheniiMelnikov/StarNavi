from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post
from comments.models import Comment
from django.utils import timezone
import datetime

User = get_user_model()


class CommentsDailyBreakdownTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.post = Post.objects.create(title="Test post", content="Test string", author=self.user)
        self.analytics_url = reverse("comments-daily-breakdown")  # Ensure this name matches your urls.py

        # Create comments with timezone-aware datetimes in UTC
        Comment.objects.create(
            post=self.post,
            content="Comment 1",
            author=self.user,
            created_at=timezone.make_aware(datetime.datetime(2024, 1, 1, 12, 0, 0), datetime.timezone.utc),
        )
        Comment.objects.create(
            post=self.post,
            content="Comment 2",
            author=self.user,
            is_blocked=True,
            created_at=timezone.make_aware(datetime.datetime(2024, 1, 1, 13, 0, 0), datetime.timezone.utc),
        )
        Comment.objects.create(
            post=self.post,
            content="Comment 3",
            author=self.user,
            created_at=timezone.make_aware(datetime.datetime(2024, 1, 2, 14, 0, 0), datetime.timezone.utc),
        )

    def test_comments_daily_breakdown_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(f"{self.analytics_url}?date_from=2024-01-01&date_to=2024-01-02")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [
            {"date": "2024-01-01", "total_comments": 2, "blocked_comments": 1},
            {"date": "2024-01-02", "total_comments": 1, "blocked_comments": 0},
        ]
        self.assertEqual(response.json(), expected_data)

    def test_comments_daily_breakdown_unauthenticated(self):
        response = self.client.get(f"{self.analytics_url}?date_from=2024-01-01&date_to=2024-01-02")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comments_daily_breakdown_missing_parameters(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.analytics_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "Parameters date_from and date_to are required"})

    def test_comments_daily_breakdown_invalid_date_format(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(f"{self.analytics_url}?date_from=2024-01-01&date_to=invalid-date")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"error": "Invalid date format. Please use YYYY-MM-DD"})
