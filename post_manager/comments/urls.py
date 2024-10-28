from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, AutoReplyViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"auto-replies", AutoReplyViewSet, basename="auto-reply")

urlpatterns = [
    path("", include(router.urls)),
]
