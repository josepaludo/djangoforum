from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):

    name = models.CharField(max_length=120)
    description = models.CharField(max_length=1000)

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_groups"
    )
    admins = models.ManyToManyField(User, related_name="admin_groups")
    members = models.ManyToManyField(User, related_name="member_groups")
    blockeds = models.ManyToManyField(User, related_name="been_blocked_groups")

    class Meta:
        ordering = ['-id']


class InviteLink(models.Model):

    id = models.UUIDField(
            primary_key=True,
            default=uuid4,
            editable=False,
        )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
