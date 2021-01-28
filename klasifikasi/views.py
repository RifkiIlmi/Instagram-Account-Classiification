from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages

from .forms import klasifikasiForms

import yaml
import json

import pandas as pd
import numpy as np
from time import time
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn import metrics
# splitting X and y into training and testing sets 
from sklearn.model_selection import train_test_split 

from data.models import Data
from preprocessing.models import Preprocessing
from pembobotan.models import Pembobotan, Bigram
from .models import Klasifikasi, KlasifikasiWbigram, HasilAkhir

# Create your views here.
def index(request):

    context = {
        'form' : klasifikasiForms,
        'name' : 'Klasifikasi',
        'title': 'Klasifikasi - Instagram Market Classification'
    }
    return render(request,'klasifikasi/index.html',context)

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

def analyze(request):
    ratio = request.POST.get('ratio', None)
    ngram = request.POST.get('ngram')

    # nilai treshold START
    # treshold = float(request.POST.get('treshold', None))

    # if treshold == 0:
    #     treshold = float(0.1)
    # nilai treshold END
    # print(float(ratio))
 
    if ratio == '-' or ngram == '-':
        messages.add_message(request, messages.WARNING, 'Pilih Rasio / N-Gram !')
        return redirect('klasifikasiIndex') # return response as JSON

    if ngram == 'uni':
        data = Klasifikasi.objects.all()
        df = pd.DataFrame(list(data.values()))

        cleanedData = Preprocessing.objects.all()
        preData = pd.DataFrame(list(cleanedData.values()))

        preToken = preData['caption_pre'].to_list()

        tokenize = []

        for i in preToken:
            item = i.split()    
            tokenize.append(item)

        preData['tokened'] = tokenize

        preData['tf'] = preData['tokened'].apply(calc_TF)

        DF_count = calc_DF(preData['tf'])
        # print(df)
        tfidfdict = df["tf_idf_dict"]
    else:
        data = KlasifikasiWbigram.objects.all()
        df = pd.DataFrame(list(data.values()))

        cleanedData = Preprocessing.objects.all()
        preData = pd.DataFrame(list(cleanedData.values()))

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
        tfidfdict = df["bgtfidf_dict"]

    sorted_DF = sorted(DF_count.items(), key=lambda kv: kv[1], reverse=True)[:50]

    # Create a list of unique words from sorted dictionay `sorted_DF`
    unique_term = [item[0] for item in sorted_DF]

    toptfidf = []
    for i in range(len(tfidfdict)):
        dt = tfidfdict[i]
        dx = yaml.load(dt)
        toptfidf.append(dx)
    
    topyt = pd.DataFrame({'tfidftop':toptfidf})

    # print(type(topyt['tfidftop'][3]))

    def calc_TF_IDF_Vec(__TF_IDF_Dict):
        TF_IDF_vector = [0.0] * len(unique_term)

        # For each unique word, if it is in the review, store its TF-IDF value.
        for i, term in enumerate(unique_term):
            if term in __TF_IDF_Dict:
                TF_IDF_vector[i] = __TF_IDF_Dict[term]
        return TF_IDF_vector
        
    df["TF_IDF_Vec"] = topyt['tfidftop'].apply(calc_TF_IDF_Vec)

    arrData = df["TF_IDF_Vec"].to_numpy()

    listData = []
    for i in range(len(arrData)):
        listData.append(arrData[i])
    
    newData = pd.DataFrame(listData, columns=unique_term)

    datasets = Data.objects.all() 
    label = pd.DataFrame(list(datasets.values()))

    newData['label'] = label['label']
    newData['id'] = preData['id']

    X = newData.drop(['label','id'], axis=1)
    y = newData['label']

    # pembagian data
    if ngram == 'uni':
        X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=float(ratio), random_state=6) 
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=float(ratio), random_state=42) 
        

    # MOdel 
    # pakai treshold START
    # naive_bayes_classifier = GaussianNB(var_smoothing=treshold)
    # pakai treshold END

    # Ndak pakai treshold START
    naive_bayes_classifier = GaussianNB()
    # Ndak pakai treshold END

    naive_bayes_classifier.fit(X_train, y_train)

    y_pred = naive_bayes_classifier.predict(X_test)
    # y_pred1 = (naive_bayes_classifier.predict_proba(X_test)[:,1] >= 0.3).astype(bool)

    # print('egegegegeg',treshold)
    # print('hfggdsf',ratio)
    # print('y1',y_pred)

    akurasi = metrics.accuracy_score(y_test, y_pred)

    CM = metrics.confusion_matrix(y_test, y_pred)
    terklasifikasi = CM[0][0]+CM[1][1]+CM[2][2]
    salahKelas = CM[0][1]+CM[0][2]+CM[1][0]+CM[1][2]+CM[2][0]+CM[2][1]

    precision = metrics.precision_score(y_test, y_pred,average=None)
    recall = metrics.recall_score(y_test, y_pred,average=None)

    X_test['id'] = newData['id']
    X_test['oldLabel'] = y_test
    X_test['newLabel'] = y_pred

    right = X_test[['id','oldLabel','newLabel']]
    # print(right)

    # get data instagram 
    dataSatu = Data.objects.all()
    dInsta = pd.DataFrame(list(dataSatu.values()))

    # get data preprocessing 
    dataDua = Preprocessing.objects.all()
    dPreproc = pd.DataFrame(list(dataDua.values()))

    satuDua = dInsta.join(dPreproc)

    resultOne = satuDua[['id','link','caption','username']]

    finalResult = pd.merge(resultOne,right, how='inner',on='id')

    finalaData = finalResult.to_numpy()

    finalDf = pd.DataFrame(finalaData.tolist(), columns=['id','link','caption','username','labelOld','labelNew'])
    # print(finalDf)
    cekDataHasil = HasilAkhir.objects.all().count()

    if cekDataHasil > 0:
        HasilAkhir.objects.all().delete()
        for hasil in finalDf.itertuples():
                hasilakhir = HasilAkhir.objects.create(
                    link=hasil.link,
                    caption=hasil.caption,
                    username=hasil.username,
                    labelold=hasil.labelOld,
                    labelnew=hasil.labelNew
                )
    else:
        for hasil in finalDf.itertuples():
                hasilakhir = HasilAkhir.objects.create(
                    link=hasil.link,
                    caption=hasil.caption,
                    username=hasil.username,
                    labelold=hasil.labelOld,
                    labelnew=hasil.labelNew
                )
        
    if request.is_ajax():
        response = {
            'totalData' : len(newData),
            'totalTest' : len(X_test),
            'totalTrain' : len(X_train),
            'akurasi': akurasi*100,
            'ratio': ratio,
            'terklasifikasi': int(terklasifikasi),
            'salahKelas': int(salahKelas),
            'cmElek' : CM[0].tolist(),
            'cmPakai' : CM[1].tolist(),
            'cmKosm' : CM[2].tolist(),
            'precision' : precision.tolist(),
            'recall' : recall.tolist(),
            'hasilAkhir': finalaData.tolist(),
            # 'result': arrRes,
        }
        return JsonResponse(response) # return response as JSON

def summary(request):
    if request.is_ajax and request.method == "GET":

        usernameSql = HasilAkhir.objects.values_list('username').order_by('username')
        username = pd.DataFrame(list(usernameSql), columns=['username'])
        username.drop_duplicates(inplace=True)        
        # username = df.username.to_dict()

        labelSql = HasilAkhir.objects.values_list('username','labelnew')
        label = pd.DataFrame(list(labelSql), columns=['username','labelnew'])

        labelPerUser = {}
        for i in username.username.to_numpy():
            count = label.loc[label['username'] == i].groupby(['labelnew']).agg({'username':'size'}).rename(columns={'username':'count'}).reset_index()
            labelPerUser[i] = count.values.tolist()
            
        
        # print(labelPerUser)

        data = {'status':1,'message':'Success','username':username.values.tolist(),'label':labelPerUser}
        # print(data)
        return JsonResponse({'data': data}, status=200)
    else:
        data = {'status':9,'message':'Error'}
        # print(data)
        return JsonResponse({'data': data}, status=200)

    return JsonResponse({}, status = 400)