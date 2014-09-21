from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
        Stores the categories to be shown in the Blog app
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, related_name="created_category")

class Feed(models.Model):
    """
        A particular blog  feed under a category
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, related_name="created_feeds")
    link = models.URLField()
