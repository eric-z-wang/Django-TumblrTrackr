# Define all the databases needed, each database will be created as
# 'trackr_[class name], ex. class Blog will be created as trackr_blog.

from django.db import models
from django.http import HttpResponse


#Table that contains all the posts being tracked
class Post(models.Model):
    url = models.TextField()
    date = models.DateTimeField()
    last_track = models.DateTimeField()
    image = models.TextField() # url to the img
    note_count = models.IntegerField()
    note_inc = models.IntegerField()
    text = models.TextField()
    times_tracked = models.IntegerField(default=1, blank=True)
    
    def __unicode__(self):
        return self.url

#Table that contains tracking infomation on all the psots
class Tracking(models.Model):
    post = models.ForeignKey(Post)
    timestamp = models.DateTimeField()
    sequence = models.IntegerField()


#Table of all the blogs being tracked
class Blog(models.Model):
    host_name = models.TextField(primary_key=True)
    likes = models.ManyToManyField(Post)
    
    def __unicode__(self):
        return self.host_name
    
    
