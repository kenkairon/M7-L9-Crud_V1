from django.db import models

class Link(models.Model):
    url = models.URLField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.url
