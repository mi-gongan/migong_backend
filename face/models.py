from django.db import models

# Create your models here.


class faceModel(models.Model):
    testfield = models.CharField(max_length=200)
    photo = models.FileField()

    def __str__(self) -> str:
        return self.testfield
