from django.shortcuts import render, redirect, get_object_or_404
from .models import Budget, Transaction
from .forms import BudgetForm, TransactionForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required(login_url='login')
def profile(request):
    template_data = {'title': 'Profile'}
    return render(request, 'finances/profile.html', {
        'template_data': template_data})

@login_required(login_url='login')
def budgets(request):
    template_data = {'title': 'Budgets'}
    return render(request, 'finances/budgets.html', {
        'template_data': template_data})

@login_required(login_url='login')
def budgets_form(request):
    template_data = {'title': 'Budgets'}
    if request.method == 'GET':
        template_data['form'] = BudgetForm()
        return render(request, 'finances/budgetsForm.html', {
            'template_data': template_data})
    elif request.method == 'POST':
        budget_form = BudgetForm(request.POST, error_class=CustomErrorList)

        if budget_form.is_valid():
            transaction = budget_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('finances.budgets')
        else:
            template_data['form'] = budget_form
            return render(request, 'finances/budgetsForm.html', {
                'template_data': template_data})

@login_required(login_url='login')
def transactions(request):
    template_data = {'title': 'Transactions'}
    return render(request, 'finances/transactions.html', {
        'template_data': template_data})

@login_required(login_url='login')
def transactions_form(request):
    template_data = {'title': 'Transactions'}
    if request.method == 'GET':
        template_data['form'] = TransactionForm()
        return render(request, 'finances/transactionsForm.html', {
            'template_data': template_data})
    elif request.method == 'POST':
        transaction_form = TransactionForm(request.POST, error_class=CustomErrorList)

        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('finances.transactions')
        else:
            template_data['form'] = transaction_form
            return render(request, 'finances/transactionsForm.html', {
                'template_data': template_data})

@login_required(login_url='login')
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if request.method == "POST":
        transaction.delete()
        return redirect('finances.transactions')

@login_required(login_url='login')
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    template_data = {'title': 'Edit Transaction'}


    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, error_class=CustomErrorList)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('finances.transactions')
        template_data['form'] = form
    else:
        template_data['form'] = TransactionForm(instance=transaction)

    return render(request, 'finances/transactionsEditForm.html',
                  {'template_data': template_data, 'transaction': transaction})

@login_required(login_url='login')
def progress(request):
    template_data = {'title': 'Progress'}
    return render(request, 'finances/progress.html', {
        'template_data': template_data})
