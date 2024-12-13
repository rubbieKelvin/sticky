# Generated by Django 5.1.4 on 2024-12-13 11:48

import api.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Clipboard",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("text", models.TextField(max_length=100000)),
                (
                    "public_id",
                    models.CharField(default=api.models.generate_pid, max_length=9),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("view_once", models.BooleanField(default=True)),
            ],
        ),
    ]