from django.db import models

class CheckActiveManager(models.Manager):
    def get_query_set(self):
        return super(CheckActiveManager, self).get_query_set().filter(is_active=True)
