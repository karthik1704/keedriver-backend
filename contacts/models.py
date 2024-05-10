from django.db import models

class contact(models.Model):

    name=models.CharField(max_length=200,null=True)
    Email=models.EmailField(max_length=30)
    Phone=models.CharField(max_length=50)
    Message=models.TextField(blank=True)

    def __str__(self):
        return self.name
    



