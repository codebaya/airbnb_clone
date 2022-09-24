from django.db import models


# Create your models here.
class CommonModel(models.Model):
    """ CommonModel Definition """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ''' this will not be saved at DB'''

    class Meta:
        abstract = True
