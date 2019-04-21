from django import forms

class AgroglifoForm(forms.Form):
    cidade = forms.CharField(required=True)
    estado = forms.CharField(required=True)
    data = forms.DateField()
    descricao = forms.CharField(required=False)
