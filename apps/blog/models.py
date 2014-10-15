from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
        Stores the categories to be shown in the Blog app
    """
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Feed(models.Model):
    """
        A particular blog  feed under a category
    """
    name = models.CharField(max_length=50)
    link = models.URLField()
    category = models.ManyToManyField(Category, related_name="feeds")

    def __unicode__(self):
        return self.name


