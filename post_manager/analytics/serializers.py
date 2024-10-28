from rest_framework import serializers


class CommentsDailyBreakdownSerializer(serializers.Serializer):
    date = serializers.DateField(source="created_at__date")
    total_comments = serializers.IntegerField()
    blocked_comments = serializers.IntegerField()
