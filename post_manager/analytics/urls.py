from django.urls import path
from .views import CommentsDailyBreakdownView

urlpatterns = [
    path("comments-daily-breakdown/", CommentsDailyBreakdownView.as_view(), name="comments-daily-breakdown"),
]
