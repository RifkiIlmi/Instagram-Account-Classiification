from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Data(models.Model):
    link = models.CharField(max_length=100, primary_key=True)
    caption = models.TextField()
    username = models.CharField(max_length=225)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.link
    
    class Meta:
        db_table = "data_instagram"