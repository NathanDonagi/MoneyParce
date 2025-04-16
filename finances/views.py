from django.shortcuts import render, redirect, get_object_or_404
from .models import Budget, Transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required(login_url='login')
def profile(request):
    template_data = {}
    template_data['title'] = 'Profile'
    return render(request, 'finances/profile.html', {
        'template_data': template_data})

@login_required(login_url='login')
def budgets(request):
    template_data = {}
    template_data['title'] = 'Budgets'
    return render(request, 'finances/budgets.html', {
        'template_data': template_data})

@login_required(login_url='login')
def transactions(request):
    template_data = {}
    template_data['title'] = 'Transactions'
    return render(request, 'finances/transactions.html', {
        'template_data': template_data})

@login_required(login_url='login')
def progress(request):
    template_data = {}
    template_data['title'] = 'Progress'
    return render(request, 'finances/progress.html', {
        'template_data': template_data})

@login_required(login_url='login')
def advice(request):
    template_data = {}
    template_data['title'] = 'Advice'
    return render(request, 'finances/advice.html', {
        'template_data': template_data})
