from django import forms

RATIO = (
  ('Choose',
      (
        ('-','-'),
        (0.3,'70:30'),
        (0.2,'80:20'),
        (0.1,'90:10'),
      )
   ),
)

NGRAM = (
  ('Choose',
      (
        ('-','-'),
        ('uni','Unigram'),
        ('bi','Bigram'),
      )
   ),
)

class klasifikasiForms(forms.Form):
    ratio = forms.ChoiceField(widget=forms.Select(attrs={'id':'ratio','class':'form-control'}), choices=RATIO)
    ngram = forms.ChoiceField(widget=forms.Select(attrs={'id':'ngram','class':'form-control'}), choices=NGRAM)
    treshold = forms.FloatField(max_value=1, min_value=0, widget=forms.NumberInput(attrs={'id':'treshold','class':'form-control','step': "0.01"}))

 
        