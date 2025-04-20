from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from .models import Budget, Transaction

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert"> {e}</div>' for e in self]))


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ("name", "category", "limit", "expense")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("name", "category", "description", "amount", "isExpense")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None