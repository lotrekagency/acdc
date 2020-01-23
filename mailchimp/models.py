from django.db import models
from core.models import Project
from mailchimp.actions import register_store
from django.core.exceptions import ValidationError

# Create your models here.
class List(models.Model):
    unique_id = models.CharField(max_length=20)
    currency_code = models.CharField(max_length=3)
    project = models.OneToOneField(Project, on_delete=models.CASCADE)

    def full_clean(self, *args, **kwargs):
        if not self.project.token:
            self.project.token = Project.generate_token()[:50]

        ok, message = register_store(self.project)
        if not ok:
            raise ValidationError(message)