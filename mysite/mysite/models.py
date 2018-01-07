from django.db import models
import json
class Project(models.Model):
    fullname=models.CharField(max_length=200)
    description=models.CharField(max_length=500)
    url=models.CharField(max_length=500)
    language=models.CharField(max_length=20)
    stargazers_count=models.IntegerField(default=0)
    forks_count=models.IntegerField(default=0)
    pushed_at=models.DateField()