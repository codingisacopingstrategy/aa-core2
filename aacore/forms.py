from django import forms


class ResourceForm(forms.Form):
    node = forms.CharField()
