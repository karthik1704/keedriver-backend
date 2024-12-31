from django.db import models
from django_prose_editor.sanitized import SanitizedProseEditorField


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    pin = models.BooleanField(default=False)
    image = models.ImageField()
    description = models.TextField()
    content = SanitizedProseEditorField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
