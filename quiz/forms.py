from django import forms

class StartForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
