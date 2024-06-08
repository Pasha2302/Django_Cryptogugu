from django.db import models
import uuid

from django.db.models import QuerySet


class UserSettingsManager(models.Manager):
    pass


class UserSettings(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    per_page = models.PositiveIntegerField(default=10)

    objects: QuerySet = UserSettingsManager()  # Явное определение менеджера

    def __str__(self):
        return f"Settings for user {self.user_id}"
