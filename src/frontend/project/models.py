from django.db import models
from django.contrib.auth.models import User
import requests


class Pad(models.Model):
    url = models.URLField(max_length=255)
    project = models.ManyToManyField('Project', null=True)

    
    @property
    def markdown(self):
        response = requests.get("%s/download" % (self.url,))
        return response.text
    
    @staticmethod
    def from_markdown(request, markdown):
        pad = Pad()
        newpad = requests.post('http://%s/new' % (request.get_host().replace('12345', '12346'),), allow_redirects=False, data=markdown, headers={'Content-Type': 'text/markdown'})
        pad.url = newpad.next.url
        return pad

    

class Project(models.Model):
    title = models.CharField(max_length=255)
    users = models.ManyToManyField(User)



# Create your models here.
