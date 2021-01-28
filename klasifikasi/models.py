from django.db import models

# Create your models here.
from django.db import models

from preprocessing.models import Preprocessing

# Create your models here.

class Klasifikasi(models.Model):
    tf_idf_dict = models.TextField() 
    id_pre_fk = models.ForeignKey(Preprocessing, on_delete=models.CASCADE)

    def __str__(self):
        return self.tf_idf_dict
    
    class Meta:
        db_table = "klasifikasi"

class KlasifikasiWbigram(models.Model):
    bgtfidf_dict = models.TextField() 
    id_pre_fk = models.ForeignKey(Preprocessing, on_delete=models.CASCADE)

    def __str__(self):
        return self.bgtfidf_dict
    
    class Meta:
        db_table = "bigramklasifikasi"

class HasilAkhir(models.Model):
    link = models.CharField(max_length=100, primary_key=True)
    caption = models.TextField()
    username = models.CharField(max_length=225)
    labelold = models.CharField(max_length=100)
    labelnew = models.CharField(max_length=100)
    

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "hasil_akhir"
