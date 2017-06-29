from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Post(models.Model):
    author = models.TextField(User, default="admin")
    text = models.TextField(null=True)
    email = models.TextField(null=True)
    password = models.TextField(null=True)

    # Time is a rhinocerous
    updated = models.DateTimeField(null=True)
    created = models.DateTimeField(null=True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return self.text+' - '+self.author.username
