from django.db import models
# from .models import File

class DataFile(models.Model):
    created = models.DateTimeField(auto_now=True)
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name
