from django import forms

class prediksiForms(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'id':'text','class':'form-control'}))


        