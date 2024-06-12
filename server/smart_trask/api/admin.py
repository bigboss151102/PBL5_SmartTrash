from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(Garbage)
admin.site.register(GarbageCompartment)
admin.site.register(PredictInfo)
admin.site.register(Notify)