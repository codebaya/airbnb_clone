from django.db import models

from common.models import CommonModel


# Create your models here.

class Category(CommonModel):
    """ Room or Experience Category """

    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "Rooms"
        EXPERIENCE = "experience", "Experiences"

    name = models.CharField(max_length=250, )
    kind = models.CharField(max_length=30, choices=CategoryKindChoices.choices, )

    def __str__(self):
        return f"{self.kind.title()} : {self.name}"

    class Meta:
        verbose_name_plural = "Categories"
