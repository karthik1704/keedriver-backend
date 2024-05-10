from django.db import models

class contact(models.Model):

    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=30)
    phone=models.CharField(max_length=50)
    message=models.TextField(blank=True)

    def __str__(self):
        return self.name
    



