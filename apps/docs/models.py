from django.db import models

class StoredCredential(models.Model):
    timestamp   = models.DateTimeField(auto_now_add=True)
    user_id     = models.TextField()
    credentials = models.TextField()