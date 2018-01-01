from django import forms

class SubmitUrlForm(forms.Form):
    url = forms.URLField(label='Input Url', required=True)
