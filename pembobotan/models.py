from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Pembobotan(models.Model):
    kata = models.CharField(max_length=100)
    tf = models.DecimalField(max_digits=19, decimal_places=4)
    idf = models.DecimalField(max_digits=19, decimal_places=4)


    def __str__(self):
        return self.kata
    
    class Meta:
        db_table = "pembobotan"

class Bigram(models.Model):
    bg_kata = models.CharField(max_length=100)
    bg_tf = models.DecimalField(max_digits=19, decimal_places=4)
    bg_idf = models.DecimalField(max_digits=19, decimal_places=4)


    def __str__(self):
        return self.bg_kata
    
    class Meta:
        db_table = "bigram"