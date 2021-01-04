from django.db import models
from django.contrib.auth.models import User
import json

class Paper(models.Model):
    source = models.CharField(max_length=64)
    handle = models.CharField(max_length=64)
    _metadata = models.TextField(db_column='metadata')
    user = models.ManyToManyField(User)

    @property
    def metadata(self):
        return json.loads(self._metadata)
    
    @staticmethod
    def from_dict(data):
        result = Paper()
        result.source = data['importer']
        result.handle = data['uid']
        result._metadata = json.dumps(data)

        return result

    class Meta:
        unique_together = [['source', 'handle']]
    
# Create your models here.
