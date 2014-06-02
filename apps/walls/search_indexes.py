from haystack import indexes
from models import Post
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.html import strip_tags
import json

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    subject = indexes.CharField(model_attr='subject')
    description = indexes.CharField(model_attr='description')
    created = indexes.CharField(model_attr='time_created')
    author = indexes.CharField(model_attr='by')
    wall = indexes.CharField(model_attr='wall')
    url = indexes.CharField()
    post_id = indexes.IntegerField(model_attr='pk')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_author(self, obj):
    	return obj.by.get_full_name()
    	
    def prepare_wall(self, obj):
    	return obj.wall.name

    def prepare_created(self, obj):
    	return naturaltime(obj.time_created)

    def prepare_url(self, obj):
    	return obj.get_absolute_url()

    def prepare_description(self, obj):
        return strip_tags(obj.description)