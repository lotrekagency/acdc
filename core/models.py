import requests
import secrets
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Project(models.Model):

    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    token = models.CharField(max_length=48, null=True, blank=True)
    api_url = models.URLField(max_length=250, null=True, blank=True)
    api_key = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def generate_token(cls):
        return secrets.token_urlsafe(48)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = Project.generate_token()
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)


class Customer(models.Model):
    email = models.CharField(max_length=250)
    external_id = models.CharField(max_length=250)
    active_id = models.CharField(max_length=50, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Connection(models.Model):

    service = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    external_id = models.CharField(max_length=250)
    logo_url = models.URLField(max_length=250)
    link_url = models.URLField(max_length=250)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    active_id = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ['project', 'external_id']

    def save(self, *args, **kwargs):
        payload = {
            "connection": {
                "service": self.service,
                "externalid": self.external_id,
                "name": self.name,
                "logoUrl": self.logo_url,
                "linkUrl": self.link_url
            }
        }

        headers = {'Api-Token': self.project.api_key}

        response = requests.post(self.project.api_url + '/api/3/connections', json=payload, headers=headers)

        self.active_id = response.json()['connection']['id']
        super(Connection, self).save(*args, **kwargs)
