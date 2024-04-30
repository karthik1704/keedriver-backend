from django.db import models
from django_prose_editor.sanitized import SanitizedProseEditorField


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField()
    description = models.TextField()
    content = SanitizedProseEditorField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
