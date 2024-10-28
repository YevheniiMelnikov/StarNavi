from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Count, Q
from django.utils.dateparse import parse_date

from comments.models import Comment
from .serializers import CommentsDailyBreakdownSerializer


class CommentsDailyBreakdownView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        if not date_from or not date_to:
            return Response(
                {"error": "Parameters date_from and date_to are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        date_from_parsed = parse_date(date_from)
        date_to_parsed = parse_date(date_to)

        if not date_from_parsed or not date_to_parsed:
            return Response({"error": "Invalid date format. Please use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        comments = Comment.objects.filter(created_at__date__gte=date_from_parsed, created_at__date__lte=date_to_parsed)

        analytics = (
            comments.values("created_at__date")
            .annotate(total_comments=Count("id"), blocked_comments=Count("id", filter=Q(is_blocked=True)))
            .order_by("created_at__date")
        )

        serializer = CommentsDailyBreakdownSerializer(analytics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
