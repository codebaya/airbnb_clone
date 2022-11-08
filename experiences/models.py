from django.db import models

from common.models import CommonModel


# Create your models here.

class Experience(CommonModel):
    """ Experiences Definition Model"""

    name = models.CharField(max_length=250, )
    country = models.CharField(max_length=50, default="South Korea", )
    city = models.CharField(max_length=80, default="Seoul", )
    host = models.ForeignKey("users.User", on_delete=models.CASCADE,
                             related_name="experiences", )
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250, )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk", blank=True)
    category = models.ForeignKey(
        "categories.Category",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )

    def __str__(self):
        return self.name


class Perk(CommonModel):
    """ What's included on Experiences """
    name = models.CharField(max_length=100, )
    details = models.CharField(max_length=250, blank=True, null=True, )
    explanation = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name
