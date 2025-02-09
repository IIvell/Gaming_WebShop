from django import forms
from .models import Igrica

class RatingForm(forms.ModelForm):
    class Meta:
        model = Igrica
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)])
        }