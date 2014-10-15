from django.db import models

class CheckActiveManager(models.Manager):
    def get_query_set(self):
        return super(CheckActiveManager, self).get_query_set().filter(is_active=True)
    def as_choices(self):
        for profile in self.all():
            yield (profile.pk, unicode(profile))
