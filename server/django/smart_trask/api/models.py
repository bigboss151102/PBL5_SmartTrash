from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class GarbageInfo(models.Model):
    type_garbage_predict = models.CharField(
        max_length=255, null=True, blank=False)
    image_garbage_predict = models.ImageField(
        upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    predict_precent = models.FloatField(default=0.0)
    manager_by = models.ForeignKey(
        User, related_name='user_w_garbage_info', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.manager_by and self.type_garbage_predict:
            return str(self.id) + '_' + self.type_garbage_predict + '_' + str(self.manager_by)
        return self.id
