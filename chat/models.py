from django.db import models

from django.contrib.auth.models import User
from main.models import BasicUser, Image, Location
import uuid

# Create your models here.


class ThreadManager(models.Manager):
    def add(self, *objs):
        for obj in objs:
            if obj not in self.all():
                self._add_items(self.source_field_name, self.target_field_name, *objs)


class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(BasicUser)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ThreadManager()


class ChatMessage(models.Model):
    thread = models.ForeignKey(
        Thread,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="chatmessage_thread",
    )
    user = models.ForeignKey(BasicUser, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    attached_images = models.ManyToManyField(Image)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
