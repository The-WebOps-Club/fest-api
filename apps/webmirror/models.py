from django.db import models


class DataBlob( models.Model ):
	data = models.TextField( max_length = 5000 )
	ref = models.CharField( max_length = 10 )
	cluster = models.CharField( max_length = 5 )
	def __unicode__(self):
		return format(self.pk) + ':' + self.data