import pandas as pd
import numpy as np
import re, string
import os
import pickle

from django.shortcuts import render

from .forms import prediksiForms

# Create your views here.
def index(request):
    context = {
        'form' : prediksiForms,
        'name' : 'Prediksi',
        'subname' : 'before',
        'title': 'Prediksi - Instagram Market Classification'
    }
    return render(request,'prediksi/index.html',context)

def predict(request):
    text = request.POST.get('text', None)

    df = pd.DataFrame([text],columns=['caption'])

    """
    ALL NEEDED FUNCTION HERE :
                |
                |
                |
                |
                V
    """

    def deEmojify(text):
        regrex_pattern = re.compile(pattern = "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002500-\U00002BEF"  # chinese char
            u"\U00002702-\U000027B0"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U00010000-\U0010ffff"
            u"\u2640-\u2642" 
            u"\u2600-\u2B55"
            u"\u200d"
            u"\u23cf"
            u"\u23e9"
            u"\u231a"
            u"\ufe0f"  # dingbats
            u"\u3030"
                            "]+", flags = re.UNICODE)
        return regrex_pattern.sub(r'',text)

    def strip_links(text):
        link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links         = re.findall(link_regex, text)
        for link in links:
            text = text.replace(link[0], ', ')    
        return text

    def strip_all_entities(text):
        entity_prefixes = ['@','#','•','—','🥰','🤗','⏺','🤩','🥳','🧏','🥰','🤔','🤭','🤑']
        for separator in  string.punctuation:
            if separator not in entity_prefixes :
                text = text.replace(separator,' ')
        words = []
        for word in text.split():
            word = word.strip()
            if word:
                if word[0] not in entity_prefixes:
                    words.append(word)
        return ' '.join(words)

    def removeNumbers(text):
        return ''.join([i for i in text if not i.isdigit()])

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

    #calc TF-IDF
    def calc_TF_IDF(TF):
        TF_IDF_Dict = {}
        #For each word in the review, we multiply its tf and its idf.
        for key in TF:
            TF_IDF_Dict[key] = TF[key] * IDF[key]
        return TF_IDF_Dict

    def calc_TF_IDF_Vec(__TF_IDF_Dict):
        TF_IDF_vector = [0.0] * len(unique_term)

        # For each unique word, if it is in the review, store its TF-IDF value.
        for i, term in enumerate(unique_term):
            if term in __TF_IDF_Dict:
                TF_IDF_vector[i] = __TF_IDF_Dict[term]
        return TF_IDF_vector

    """
    END FUNCTION
    """
    
    converted = df['caption'].to_list()
    cleaned = []
    for item in converted:
        phase1 = strip_all_entities(strip_links(item))
        phase2 = deEmojify(phase1)
        phase3 = removeNumbers(phase2)
        cleaned.append(phase3)

    df = df.drop(['caption'], axis=1)
    df['cleaned'] = cleaned
    df['cleaned'] = df['cleaned'].str.lower()
    preToken = df['cleaned'].to_list()

    tokenize = []

    for i in preToken:
        item = i.split()    
        tokenize.append(item)
    # tokenize
    df['tokened'] = tokenize
    df = df.drop(['cleaned'], axis=1)

    module_dir = os.path.dirname(__file__)
    katadasar = os.path.join(module_dir, '../preprocessing/kata_dasar.xlsx')   #full path to text.
    norm_dict = pd.read_excel(katadasar)
    kamus = dict(zip(norm_dict.tbk, norm_dict.bk))
    for i in range(len(df.index)):
        results = []
        for wrd in df['tokened'].iloc[i]: 

            # searching from lookp_dict 
            results.append(kamus.get(wrd, wrd))

        df['tokened'].iloc[i] = results


    stopwords_path = os.path.join(module_dir, '../preprocessing/stopword_list_tala.txt')   #full path to text.
    stopwords = pd.read_fwf(stopwords_path)
    stopwords =  set(stopwords.stopwords)
    for i in range(len(df.index)):
        filtered_sentence = [] 
        for w in df['tokened'].iloc[i]: 
            if w not in stopwords: 
                filtered_sentence.append(w) 
        df['tokened'].iloc[i] = filtered_sentence
        
    # import StemmerFactory class
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    # create stemmer
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    for i in range(len(df.index)):
        hasil = [] 
        for word in df['tokened'].iloc[i]: 
            stemmed = stemmer.stem(word)
            hasil.append(stemmed) 
        df['tokened'].iloc[i] = hasil

    n_document = len(df)
    unique_term = ['harga','ya','wa','pakai','kulit','info','order','no','lengkap','klik','warna','shopee','link','produk','bahan','bio','wajah','aman','kaos','cotton','gb','langsung','yuk','sablon','minggu','rp','size','kualitas','satu','up','iphone','bandung','milik','kirim','nih','material','suka','baik','sedia','banget','id','kandung','dapat','cerah','pilih','garansi','nyaman','whatsapp','cm','dm']
    df["tf_dict"] = df['tokened'].apply(calc_TF)
    DF_count = calc_DF(df["tf_dict"])
    IDF = calc_IDF(n_document, DF_count)
    df["TF-IDF_dict"] = df["tf_dict"].apply(calc_TF_IDF)
    df["TF_IDF_Vec"] = df["TF-IDF_dict"].apply(calc_TF_IDF_Vec)

    arrData = df["TF_IDF_Vec"].to_numpy()
    listData = []
    for i in range(len(arrData)):
        listData.append(arrData[i])
    newData = pd.DataFrame(listData, columns=unique_term)

    # load the model from disk
    filename = 'klasifikasiAkun_model.sav'
    model_path = os.path.join(module_dir, filename)   #full path to text.
    loaded_model = pickle.load(open(model_path, 'rb'))

    result = loaded_model.predict(newData)
    # print(df)
    context = {
        'form' : prediksiForms,
        'name' : 'Prediksi',
        'subname' : 'after',
        'result' : result[0],
        'text' : text,
        'title': 'Prediksi - Instagram Market Classification'
    }
    return render(request,'prediksi/index.html',context)

