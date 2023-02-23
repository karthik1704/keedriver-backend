from django.db import models

# Create your models here.
class City(models.Model):
    name=models.CharField(max_length=150)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name
    

class Area(models.Model):
    city=models.ForeignKey(City, on_delete=models.CASCADE)
    name= models.CharField(max_length=150)

    def __str__(self):
        return self.name
    