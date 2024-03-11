from django.db import models

# Create your models here.


class GarbageInfo(models.Model):
    type_garbage = models.CharField(max_length=255, null=True, blank=False)
    image_garbage = models.ImageField(
        upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.type_garbage
