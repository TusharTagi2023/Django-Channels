from django.db import models

# Create your models here.
class Group(models.Model):
    gpname= models.CharField(max_length=50)


class Chats(models.Model):
    group = models.ForeignKey('Group',on_delete=models.CASCADE,related_name='group_chats')
    txt=models.TextField()
    user=models.CharField(max_length=100,null=True,blank=True)