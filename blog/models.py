
from distutils.command.upload import upload
from distutils.filelist import FileList
from email.policy import default
from random import choices
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from  ckeditor.fields import RichTextField
post_catagory=[
    ('sports','Sports'),
    ('technology','Technology'),
    ('movies','Movies'),
    ('science','Science'),
    ('music','Music'),
    ('exprience','Exprience'),
    ('fashion','Fashion')
]
class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,
              null=True,blank=True)
    title=models.CharField(max_length=200)
    discription=models.TextField(null=True,blank=True)
    body=RichTextField(blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    image=models.ImageField(null=True,blank=True,upload_to='image')
    catagory=models.CharField(max_length=200,choices=post_catagory)
    liked=models.ManyToManyField(User,default=None,related_name='liked',blank=True)
    unliked=models.ManyToManyField(User,default=None,related_name='unliked',blank=True)
    def __str__(self):
        return self.title
    @property
    def num_like(self):
        return self.like.all().count()  
    class Meta:
        ordering=['-created']  
LIKE_CHOICES=(
    ('like','like'),
    ('unlike','Unlike')
)
class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    value=models.CharField(choices=LIKE_CHOICES,default='like',max_length=10)
    def __str__(self):
         return str(self.post)
class Dislike(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.post)     
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    photo=models.ImageField(default='defualt.png',upload_to='image')
    def __str__(self):
        return f'{self.user} Profile'
class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True,blank=True)
    post=models.ForeignKey(Post,related_name='comment',on_delete=models.CASCADE)
    body=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-date_added']
    def __str__(self):
        return f'{self.post.title,self.user}'

