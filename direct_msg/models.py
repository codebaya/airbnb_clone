from django.db import models

from common.models import CommonModel


# Create your models here.

class ChattingRoom(CommonModel):
    """ Room Model Definition """
    users = models.ManyToManyField(
        "users.User",
    )

    def __str__(self):
        return "ChattingRoom"


class Message(CommonModel):
    """ Message Model Definition """
    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="direct_msgs",
    )
    room = models.ForeignKey(
        "direct_msg.ChattingRoom",
        on_delete=models.CASCADE,
        related_name="direct_msgs",
    )

    def __str__(self):
        return f"{self.user} says : {self.text}"
