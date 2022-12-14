from django.db import models

from common.models import CommonModel
from experiences.models import Experience


# Create your models here.

class Photo(CommonModel):
    file = models.URLField()
    description = models.CharField(max_length=140, )
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, blank=True, null=True, related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience", on_delete=models.CASCADE, related_name="photos",
    )

    def __str__(self):
        return "Photo File"


class Video(CommonModel):
    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="medias",
    )

    def __str__(self):
        return "Video File"
