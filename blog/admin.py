from django.contrib import admin
from . import models

class AdminTask(admin.ModelAdmin):
    list_display=['title','created','updated','catagory']
class AdminReply(admin.ModelAdmin):
    list_display=['comment','reply','reply_date','user']   
admin.site.register(models.Post,AdminTask)
admin.site.register(models.Profile)
admin.site.register(models.Comment)
admin.site.register(models.Like)
admin.site.register(models.Dislike)
admin.site.register(models.Reply,AdminReply)
