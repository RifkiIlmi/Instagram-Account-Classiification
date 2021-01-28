from django.db import models

# Create your models here.
from django.db import models

from data.models import Data

# Create your models here.

class Preprocessing(models.Model):
    caption_pre = models.TextField()
    link_fk = models.ForeignKey(Data, on_delete=models.CASCADE)

    def __str__(self):
        return self.link_fk
    
    class Meta:
        db_table = "preprocessing"