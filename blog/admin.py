from django.contrib import admin
from . import models

class AdminTask(admin.ModelAdmin):
    list_display=['title','created','catagory']

admin.site.register(models.Post,AdminTask)
admin.site.register(models.Profile)
admin.site.register(models.Comment)
