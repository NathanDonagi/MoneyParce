from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
import json

from finances.models import Transaction, Category, Budget

@login_required
def financial_reports(request):
    """View for displaying financial reports and visualizations."""
    # Get date range for filtering
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)  # Last 30 days by default
    
    # Get transactions for the period
    transactions = Transaction.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    )
    
    # Calculate total income and expenses
    total_income = transactions.filter(isExpense=False).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(isExpense=True).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get category-wise expenses
    category_expenses = {}
    for category in Category.objects.filter(user=request.user):
        amount = transactions.filter(category=category, isExpense=True).aggregate(Sum('amount'))['amount__sum'] or 0
        if amount > 0:
            category_expenses[category.name] = amount
    
    # Prepare data for charts
    chart_data = {
        'categories': list(category_expenses.keys()),
        'expenses': list(category_expenses.values()),
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': total_income - total_expenses
    }
    
    context = {
        'chart_data': json.dumps(chart_data),
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': total_income - total_expenses,
        'category_expenses': category_expenses,
    }
    
    return render(request, 'reports/financial_reports.html', context)

@login_required
def spending_trends(request):
    """View for displaying spending trends over time."""
    # Get date range for filtering
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=90)  # Last 90 days
    
    # Get daily spending data
    daily_spending = {}
    current_date = start_date
    while current_date <= end_date:
        amount = Transaction.objects.filter(
            user=request.user,
            date=current_date,
            isExpense=True
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        daily_spending[current_date.strftime('%Y-%m-%d')] = amount
        current_date += timedelta(days=1)
    
    # Get monthly spending data
    monthly_spending = {}
    current_date = start_date
    while current_date <= end_date:
        month_key = current_date.strftime('%Y-%m')
        amount = Transaction.objects.filter(
            user=request.user,
            date__year=current_date.year,
            date__month=current_date.month,
            isExpense=True
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_spending[month_key] = amount
        current_date += timedelta(days=32)  # Move to next month
    
    context = {
        'daily_spending': json.dumps(daily_spending),
        'monthly_spending': json.dumps(monthly_spending),
    }
    
    return render(request, 'reports/spending_trends.html', context) 