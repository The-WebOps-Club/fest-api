from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    """
        A particular blog  feed under a category
    """
    name = models.CharField(max_length=50)
    link = models.URLField()

    def __unicode__(self):
        return self.name

class Category(models.Model):
    """
        Stores the categories to be shown in the Blog app
    """
    name = models.CharField(max_length=50)
    feeds = models.ManyToManyField(Feed, related_name="feeds", blank=True, null=True)
    def __unicode__(self):
        return self.name

