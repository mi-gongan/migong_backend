from django.db import models

# Create your models here.


class test(models.Model):
    testfield = models.CharField(max_length=200)
    photo = models.FileField(upload_to='')

    def __str__(self) -> str:
        return self.testfield
