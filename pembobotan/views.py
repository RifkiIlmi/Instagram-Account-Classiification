from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages

import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
# from tqdm import tqdm

from data.models import Data
from preprocessing.models import Preprocessing
from .models import Pembobotan
from .models import Bigram
from klasifikasi.models import Klasifikasi
from klasifikasi.models import KlasifikasiWbigram


# Create your views here.
def index(request):
    cekData = Pembobotan.objects.count() 
    cekDataBg = Bigram.objects.count() 

    # print(cekData)
    if cekData < 0 :
        context = {
            'name' : 'Pembobotan',
            'title': 'Pembobotan - Instagram Market Classification'
        }
        return render(request,'pembobotan/index.html',context)
    else:
        if cekDataBg < 0:
            data = Pembobotan.objects.all()[:1000]
            context = {
                'data': data,
                'name' : 'Pembobotan',
                'title': 'Pembobotan - Instagram Market Classification'
            }
            return render(request,'pembobotan/index.html',context)
        else:
            data = Pembobotan.objects.all()[:1000]
            dataBg = Bigram.objects.all()[:1000]
            context = {
                'data': data,
                'databg' : dataBg,
                'name' : 'Pembobotan',
                'title': 'Pembobotan - Instagram Market Classification'
            }
            return render(request,'pembobotan/index.html',context)

"""
    Tahap Dibawah digunakan untuk menghitung TF, IDF, dan TF-Idf
    step:
    1.Hitung TF
    2.Hitung DF
    3.Hitung IDF
    4.Hitung Tf-Idf (perhitungan Tf-Idf dilakukan didalam tiap-tiap fungsi pembobotan)
    |
    |
    |
    v
"""

def calc_TF(document):
    # Hitung berapa banyak kata muncul pada captiom
    TF_dict = {}
    for term in document:
        if term in TF_dict:
            TF_dict[term] += 1
        else:
            TF_dict[term] = 1
    # Masukkan rumus perhitungan TF
    for term in TF_dict:
        TF_dict[term] = TF_dict[term] / len(document)
    return TF_dict

def calc_DF(tfDict):
    count_DF = {}
    # hitung jumlah kemunculan kata pada seluruh data
    for document in tfDict:
        for term in document:
            if term in count_DF:
                count_DF[term] += 1
            else:
                count_DF[term] = 1
    return count_DF

def calc_IDF(__n_document, __DF_count):
    IDF_Dict = {}
    for term in __DF_count:
        IDF_Dict[term] = np.log(__n_document / (__DF_count[term] + 1))
    return IDF_Dict    

"""
    ^
    |
    |
    |
    ====== Akhir tahap perhitungan Tf-Idf =====
"""

"""
    Tahap Dibawah digunakan untuk menghitung proses pembobotan Unigram
    step:
    1.Hitung TFidf didalam fungsi bobot()
    2.Simpan perhitungan Tf-Idf kedalam Tabel klasifikasi pada fungsi saveKlasifikasi()
    3.Simpan data Tf dalam tabel bobot pada fungsi bulkSave() 
    4.Lalu update data IDF pada tabel bobot menggunakan fungsi update()
    |
    |
    |
    v
"""

def bulkSave(key,value):
    # print(key, value)
    Pembobotan.objects.create(
        kata=key,
        tf=value,
    )  

def update(key,value):
    # print(key,value)
    Pembobotan.objects.filter(kata=key).update(idf=value)

def saveKlasifikasi(data):
    # print('true')
    # print( data["TFIDF_dict"][0])
    for list in data.itertuples():
            list = Klasifikasi.objects.create(
                tf_idf_dict=list.TFIDF_dict,
                id_pre_fk_id=list.id,
            )

def bobot(request):
    cleanedData = Preprocessing.objects.all()
    preData = pd.DataFrame(list(cleanedData.values()))

    cekData = Pembobotan.objects.all().count()

    preToken = preData['caption_pre'].to_list()

    tokenize = []

    for i in preToken:
        item = i.split()    
        tokenize.append(item)

    preData['tokened'] = tokenize

    preData['tf'] = preData['tokened'].apply(calc_TF)

    DF_count = calc_DF(preData['tf'])

    n_document = len(preData)
    #Stores the idf dictionary
    IDF = calc_IDF(n_document, DF_count)
     #calc TF-IDF
    def calc_TF_IDF(TF):
        TF_IDF_Dict = {}
        #For each word in the review, we multiply its tf and its idf.
        for key in TF:
            TF_IDF_Dict[key] = TF[key] * IDF[key]
        return TF_IDF_Dict

    cekKlasifikasi = Klasifikasi.objects.count() 

    if cekKlasifikasi <=0:
        #Stores the TF-IDF Series
        preData["TFIDF_dict"] = preData["tf"].apply(calc_TF_IDF)
        saveKlasifikasi(preData)
    else:
        pass

    if cekData <=0:
        for i in range(len(preData)):
            for key in preData["tokened"][i]:
                bulkSave(key, preData['tf'][i][key])

        for x, y in IDF.items():
            update(x,y)
    else:
        messages.add_message(request, messages.WARNING, 'Data Telah Di Bobot Menggunkanan Unigram')

    return redirect('pembobotanIndex')

"""
    ^
    |
    |
    |
    ====== Akhir tahap pembobotan Unigram  =====
"""
"""
    Tahap Dibawah digunakan untuk menghitung proses pembobotan Bigram
    step:
    1.Hitung TFidf didalam fungsi bigram()
    2.Simpan perhitungan Tf-Idf kedalam Tabel bigramklasifikasi pada fungsi saveBgKlasifikasi()
    3.Simpan data Tf dalam tabel bigram pada fungsi bulkSaveBg() 
    4.Lalu update data IDF pada tabel bigram menggunakan fungsi updateBg()
    |
    |
    |
    v
"""

def bulkSaveBg(key,value):
    # print(key, value)
    Bigram.objects.create(
        bg_kata=key,
        bg_tf=value,
    )  

def saveBgKlasifikasi(data):
    # print('true')
    # print( data["TFIDF_dict"][0])
    for list in data.itertuples():
            list = KlasifikasiWbigram.objects.create(
                bgtfidf_dict=list.TFIDF_dict,
                id_pre_fk_id=list.id,
            )

def updateBg(key,value):
    # print(key,value)
    Bigram.objects.filter(bg_kata=key).update(bg_idf=value)

def bigram(request):
    cleanedData = Preprocessing.objects.all()
    preData = pd.DataFrame(list(cleanedData.values()))

    cekData = Bigram.objects.all().count()

    preToken = preData['caption_pre'].to_list()

    tokenize = []

    for i in preToken:
        item = i.split()    
        tokenize.append(item)

    preData['tokened'] = tokenize
    preData['tokened'] = preData["tokened"].str.join(" ") 

    vectorizer2 = CountVectorizer(analyzer='word', ngram_range=(2, 2))
    X2 = vectorizer2.fit_transform(preData.tokened[1199:1200])

    next = 0
    res = []
    for i in range(len(preData.tokened)):
        next = i+1
        vectorizer2.fit_transform(preData.tokened[i:next])
        res.append(vectorizer2.get_feature_names())

    preData['bigram'] = res

    preData['tf'] = preData['bigram'].apply(calc_TF)

    DF_count = calc_DF(preData['tf'])

    n_document = len(preData)
    #Stores the idf dictionary
    IDF = calc_IDF(n_document, DF_count)
     #calc TF-IDF
    def calc_TF_IDF(TF):
        TF_IDF_Dict = {}
        #For each word in the review, we multiply its tf and its idf.
        for key in TF:
            TF_IDF_Dict[key] = TF[key] * IDF[key]
        return TF_IDF_Dict

    cekKlasifikasi = KlasifikasiWbigram.objects.count() 

    if cekKlasifikasi <=0:
        #Stores the TF-IDF Series 
        preData["TFIDF_dict"] = preData["tf"].apply(calc_TF_IDF)
        saveBgKlasifikasi(preData)
    else:
        pass

    if cekData <=0:
        for i in range(len(preData)):
            for key in preData["bigram"][i]:
                bulkSaveBg(key, preData['tf'][i][key])

        for x, y in IDF.items():
            updateBg(x,y)
    else:
        messages.add_message(request, messages.WARNING, 'Data Telah Di Bobot Menggunkanan Bigram')

    return redirect('pembobotanIndex')

"""
    ^
    |
    |
    |
    ====== Akhir tahap pembobotan Bigram  =====
"""