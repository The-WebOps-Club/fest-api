from haystack import indexes
from models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # post_subject = indexes.CharField(model_attr='subject')
    # post_description = indexes.CharField(model_attr='description')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()