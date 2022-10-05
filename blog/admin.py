from django.contrib import admin
from . import models

class AdminTask(admin.ModelAdmin):
    list_display=['title','created','updated','catagory']
    
admin.site.register(models.Post,AdminTask)
admin.site.register(models.Profile)
admin.site.register(models.Comment)
admin.site.register(models.Like)
admin.site.register(models.Dislike)
admin.site.register(models.ReplyComment)
