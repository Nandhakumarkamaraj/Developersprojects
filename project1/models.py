from email.mime import image
import profile
from tkinter import CASCADE
from django.db import models
from users.models import Profile

class Project(models.Model):
    project_type = [('static','static application'),
                    ('dynamic','web application')
    ]
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField (max_length=500)
    description = models.TextField (max_length=5000,null=True,blank=True)
    image = models.ImageField (upload_to='photos/', default='photos/download.jpg',null=True,blank=True)
    demo_link = models.CharField (max_length=2000,null=True,blank=True)
    source_link = models.CharField (max_length=2000,null=True,blank=True)
    tags= models.ManyToManyField('Tag',blank=True)
    created = models.DateTimeField (auto_now_add=True)
    vote_total = models.IntegerField (default=0,null=True,blank=True)
    vote_ratio = models.IntegerField (default=0,null=True,blank=True)
    type = models.CharField (max_length=30,choices=project_type,null=True,blank=True)

    def __str__(self):
        return  str (self.title)

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalCount = reviews.count()
        voteRatio = (upVotes/totalCount)*100

        self.vote_total = totalCount
        self.vote_ratio = voteRatio
        self.save()

    def reviewers(self):
        reviewers = self.review_set.all().values_list('owner__id',flat=True)
        return reviewers       

class Review(models.Model):

    values = [('up','like'),('down','dislike')]
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    body=models.TextField(null=True,blank=True)
    value=models.CharField(max_length=50,choices=values)
    created = models.DateTimeField (auto_now_add=True)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner','project']]


class Tag(models.Model):
    name=models.CharField(max_length=500)
    created = models.DateTimeField (auto_now_add=True)

    def __str__(self):
        return self.name

# Create your models here.
