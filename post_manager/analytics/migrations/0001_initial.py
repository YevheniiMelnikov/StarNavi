# Generated by Django 5.1.2 on 2024-10-27 18:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommentAnalytics",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("total_comments", models.IntegerField(default=0)),
                ("blocked_comments", models.IntegerField(default=0)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="analytics", to="posts.post"
                    ),
                ),
            ],
        ),
    ]
