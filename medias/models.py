from django.db import models

from common.models import CommonModel
from experiences.models import Experience


# Create your models here.

class Photo(CommonModel):
    file = models.ImageField()
    description = models.CharField(max_length=140, )
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, blank=True, null=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience", blank=True, null=True, on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Photo File"


class Video(CommonModel):
    file = models.FileField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="medias",
    )

    def __str__(self):
        return "Video File"


dead = True
