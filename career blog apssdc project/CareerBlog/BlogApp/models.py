from django.db import models
from django.utils import timezone
from django import forms



class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

