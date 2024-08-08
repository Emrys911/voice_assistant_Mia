from django.db import models


class Assistant(models.Model):
    name = models.CharField(max_length=100)
    response = models.TextField()

    def __str__(self):
        return self.name
