# Generated by Django 5.1.2 on 2024-10-28 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_post_is_blocked"),
    ]

    operations = [
        migrations.CreateModel(
            name="AutoReply",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reply_content_template", models.TextField()),
                (
                    "post",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name="auto_reply", to="posts.post"
                    ),
                ),
            ],
        ),
    ]