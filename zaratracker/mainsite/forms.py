from django import forms
from .models import Reference

class CreateReferenceForm(forms.ModelForm):

    class Meta:
        model = Reference
        fields = ('reference', 'region',)