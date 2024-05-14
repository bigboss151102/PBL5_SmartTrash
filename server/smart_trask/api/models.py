from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='user_w_profile', on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.BooleanField(default=True)
    birthday = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('user',)

    def __str__(self):
        if self.user and self.phone:
            return self.user.email + "_" + self.phone
        return self.user


class Garbage(models.Model):
    user = models.ForeignKey(User, related_name='user_w_garbage',
                             on_delete=models.SET_NULL, blank=True, null=True)
    garbage_code = models.CharField(max_length=50, null=True, blank=True)
    name_country = models.CharField(max_length=50, null=True, blank=True)
    description = RichTextField(blank=True, null=True)
    distance_is_full = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        if self.user and self.name_country and self.garbage_code:
            return str(self.id) + "_" + self.user.username + "_" + self.garbage_code
        return str(self.id)


class GarbageCompartment(models.Model):
    garbage = models.ForeignKey(Garbage, related_name='garbage_w_GarbageCompartment',
                                on_delete=models.SET_NULL, blank=True, null=True)
    type_name_compartment = models.CharField(
        max_length=50, null=True, blank=True)
    distance_is_full = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        if self.garbage and self.type_name_compartment:
            return str(self.id) + "_" + self.garbage.garbage_code + "_" + self.type_name_compartment
        return str(self.id)


class PredictInfo(models.Model):
    garbage_compartment = models.ForeignKey(
        GarbageCompartment, related_name='garbage_compartment_w_predict_info', on_delete=models.SET_NULL, blank=True, null=True)
    type_name_garbage = models.CharField(max_length=50, null=True, blank=True)
    image_garbage = models.ImageField(
        upload_to='images/', null=True, blank=True)
    predict_percent = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        if self.garbage_compartment and self.type_name_garbage and self.predict_precent:
            return str(self.id) + '_' + self.garbage_compartment.type_name_compartment + '_' + str(self.predict_precent)
        return str(self.id)


# class SessionToken(models.Model):
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, primary_key=True)
#     token = models.CharField(max_length=500, null=True, blank=False)
#     hostname = models.CharField(max_length=100, null=True, blank=True)
#     ip_address = models.CharField(max_length=100, null=True, blank=True)
#     mac_address = models.CharField(max_length=100, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
