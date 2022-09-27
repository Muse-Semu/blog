
from distutils.command.upload import upload
from distutils.filelist import FileList
from django.db import models
from django.contrib.auth.models import User
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
    created=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(null=True,blank=True,upload_to='image')
    catagory=models.CharField(max_length=200,choices=post_catagory)
    like=models.ManyToManyField(User,related_name='like')


    def __str__(self):
        return self.title
    class Meta:
        ordering=['-created']    

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
        return f'{self.post.title,self.user} '

