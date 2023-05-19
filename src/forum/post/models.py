from django.db import models
from django.contrib.auth.models import User

from group.models import Group


class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)

    downvoters = models.ManyToManyField(
        User,
        related_name="downvoteds"
    )
    upvoters = models.ManyToManyField(
        User,
        related_name="upvoteds"
    )


class MainPost(Post):

    title = models.CharField(max_length=120)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="posts",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-id"]


class Answer(Post):

    related_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE, 
        related_name="answers"
    )

    class Meta:
        ordering = ["-id"]