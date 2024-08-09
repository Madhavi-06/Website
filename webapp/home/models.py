from django.db import models
import os


class Register(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)    
    age=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)

class currency(models.Model):
    image = models.ImageField(upload_to="home/static/output")

    def filename(self):
        return os.path.basename(self.image.name)
