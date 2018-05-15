from django import forms
from .models import Linguagem

class LinguagemForm(forms.ModelForm):
    class Meta:
        model = Linguagem
        fields = '__all__'
