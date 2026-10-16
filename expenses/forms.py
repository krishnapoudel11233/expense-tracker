from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta: 
        model=Expense
        fields=['title','amount', 'category', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Weekly groceries'}),
            'amount': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01', 'min': '0.01'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }