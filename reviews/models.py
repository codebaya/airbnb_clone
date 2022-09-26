from django.db import models

from common.models import CommonModel


# Create your models here.

class Review(CommonModel):
    """ Review from a user to a room or Experience """
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey(
        "rooms.Room", null=True,
        blank=True, on_delete=models.SET_NULL, )
    experience = models.ForeignKey(
        "experiences.Experience", null=True,
        blank=True, on_delete=models.CASCADE,
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} / {self.rating}"
