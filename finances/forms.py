from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from .models import Budget, Transaction, Category


class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert"> {e}</div>' for e in self]))


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Grab user if passed
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "New Category Name"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ("name", "category", "limit", "expense")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None
        self.fields['category'].queryset = Category.objects.all()


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("name", "category", "description", "amount", "isExpense", "date")
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={
                'step': '0.01',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None
        self.fields['category'].empty_label = ""
        amount = self.initial.get('amount') or getattr(self.instance, 'amount', None)
        if amount is not None:
            self.initial['amount'] = "{:.2f}".format(amount)


