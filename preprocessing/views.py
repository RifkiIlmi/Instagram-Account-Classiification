from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage

from .cleaning import deEmojify,removeNumbers,strip_all_entities,strip_links

# import StemmerFactory class
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

import os
import pandas as pd 

from data.models import Data
from .models import Preprocessing

# Create your views here.
def index(request):
    cekData = Preprocessing.objects.count()

    if cekData < 0 :
        context = {
            'name' : 'Preprocessing',
            'title': 'Preprocessing - Instagram Market Classification'
        }
        return render(request,'preprocessing/index.html',context)
    else:
        data = Preprocessing.objects.select_related('link_fk').all()
        context = {
            'data': data,
            'name' : 'Preprocessing',
            'title': 'Preprocessing - Instagram Market Classification'
        }
        return render(request,'preprocessing/index.html',context)


def bulksave(data):
    print('true')
    print(data.head(20))
    for list in data.itertuples():
            list = Preprocessing.objects.create(
                caption_pre=list.tokened,
                link_fk_id=list.link,
            )

def process(request):
    cekData = Preprocessing.objects.count()

    if cekData >0:
        messages.add_message(request, messages.WARNING, 'Data Telah Di Pre-Processing')
    else:
        df = pd.DataFrame(list(Data.objects.values()))

        converted = df['caption'].to_list()

        # Cleaning 
        cleaned = []
        for item in converted:
            phase1 = strip_all_entities(strip_links(item))
            phase2 = deEmojify(phase1)
            phase3 = removeNumbers(phase2)
            cleaned.append(phase3)
        
        df = df.drop(['caption'], axis=1)
        df['cleaned'] = cleaned

        df = df[['link','cleaned','username','label']]

        # casefolding
        df['cleaned'] = df['cleaned'].str.lower()

        # Tokenizing
        preToken = df['cleaned'].to_list()

        tokenize = []

        for i in preToken:
            item = i.split()    
            tokenize.append(item)

        df['tokened'] = tokenize
        df = df.drop(['cleaned'], axis=1)
        df = df[['link','tokened','username','label']]

        # Normalization
        module_dir = os.path.dirname(__file__)
        katadasar = os.path.join(module_dir, 'kata_dasar.xlsx')   #full path to text.
        norm_dict = pd.read_excel(katadasar)
        kamus = dict(zip(norm_dict.tbk, norm_dict.bk))

        for i in range(len(df.index)):
            results = []
            for wrd in df['tokened'].iloc[i]: 
                # searching from lookp_dict 
                results.append(kamus.get(wrd, wrd))

            df['tokened'].iloc[i] = results

        # filtering 
        stopwords_path = os.path.join(module_dir, 'stopword_list_tala.txt')   #full path to text.
        stopwords = pd.read_fwf(stopwords_path)
        stopwords =  set(stopwords.stopwords)

        for i in range(len(df.index)):
            filtered_sentence = [] 
            for w in df['tokened'].iloc[i]: 
                if w not in stopwords: 
                    filtered_sentence.append(w) 
            df['tokened'].iloc[i] = filtered_sentence
            
        # Stemming 
        # create stemmer
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        for i in range(len(df.index)):
            hasil = [] 
            for word in df['tokened'].iloc[i]: 
                stemmed = stemmer.stem(word)
                hasil.append(stemmed) 
            df['tokened'].iloc[i] = hasil
        
        df['tokened'] = df["tokened"].str.join(" ") 
        bulksave(df)
        messages.add_message(request, messages.SUCCESS, 'Data Berhasil Di Pre-Processing')
        

    return redirect('preprocessingIndex')

