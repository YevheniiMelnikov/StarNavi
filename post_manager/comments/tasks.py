import os
from contextlib import suppress

import loguru
from celery import shared_task
from django.contrib.auth import get_user_model
import openai
from posts.models import Post
from comments.models import Comment
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()
logger = loguru.logger


@shared_task
def send_auto_reply(comment_id: int) -> None:
    with suppress(Comment.DoesNotExist, Post.DoesNotExist):
        comment = Comment.objects.get(id=comment_id)
        post = comment.post

        if post.auto_reply_enabled and hasattr(post, "auto_reply"):
            try:
                reply_content = generate_ai_reply(post.content, comment.content)
                if reply_content:
                    send_mail(
                        subject="Auto reply to your comment",
                        message=reply_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[comment.author.email],
                    )
                    logger.info(f"Auto reply sent for comment ID {comment.id}")
            except Exception as e:
                logger.error(f"Error while sending auto reply to comment {comment.id}: {e}")


def generate_ai_reply(post_content: str, comment_content: str) -> str | None:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Post: {post_content}\nComment: {comment_content}\nGenerate an appropriate, polite, and relevant reply to the comment.",
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150,
        temperature=0.5,
    )
    logger.info("Auto reply generated successfully")
    return response.choices[0].message["content"].strip()
