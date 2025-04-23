import json # Add json import
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction # Import transaction
from django.db.models import Max, Sum  # Import Max
from django.template.context_processors import request
from django.views.decorators.http import require_POST, require_http_methods  # Import require_POST
from django.http import JsonResponse, HttpResponseRedirect  # Import JsonResponse
from django.utils import timezone
from datetime import timedelta


from .models import Budget, Transaction, Category
from .forms import BudgetForm, TransactionForm, CustomErrorList, CategoryForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required(login_url='login')
def profile(request):
    user = request.user
    template_data = {'title': 'Profile'}
    budgets = Budget.objects.filter(user=user)
    total_limit = budgets.aggregate(Sum('limit'))['limit__sum'] or 0
    total_expense = budgets.aggregate(Sum('expense'))['expense__sum'] or 0

    advice = [
        "Make sure to track your expenses regularly to stay on top of your budget.",
        "Consider setting up alerts when you're close to reaching your budget limits.",
        "Review your spending habits monthly to avoid unnecessary expenses."
    ]

    return render(request, 'finances/profile.html', {
        'template_data': template_data,
        'total_limit': total_limit,
        'total_expense': total_expense,
        'advice': advice,
    })


@login_required
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        form = CategoryForm(user=request.user)

    return render(request, 'finances/create_category_form.html', {'form': form})


@login_required
@require_http_methods(["DELETE"])
def delete_category(request, category_id):
    try:
        category = get_object_or_404(Category, id=category_id, user=request.user)

        # Check if category has transactions
        if category.transactions.exists():
            return JsonResponse({
                'success': False,
                'message': 'Cannot delete category with existing transactions. Please move or delete those transactions first.'
            }, status=400)

        # Check if category has budgets
        if category.budgets.exists():
            return JsonResponse({
                'success': False,
                'message': 'Cannot delete category with existing budgets. Please update or delete those budgets first.'
            }, status=400)

        category.delete()
        return JsonResponse({'success': True, 'message': 'Category deleted successfully.'})

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)


@login_required
@require_POST
def rename_category(request, category_id):
    try:
        category = get_object_or_404(Category, id=category_id, user=request.user)
        new_name = request.POST.get('new_name', '').strip()

        if not new_name:
            return JsonResponse({
                'success': False,
                'message': 'Category name cannot be empty'
            }, status=400)

        if Category.objects.filter(user=request.user, name=new_name).exclude(id=category.id).exists():
            return JsonResponse({
                'success': False,
                'message': 'A category with this name already exists'
            }, status=400)

        category.name = new_name
        category.save()

        return JsonResponse({
            'success': True,
            'message': 'Category renamed successfully'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)

@login_required
@require_POST # Ensures this view only accepts POST requests
@transaction.atomic # Ensures all updates happen or none do
def reorder_categories(request):
    try:
        # Decode JSON body expected from AJAX request
        data = json.loads(request.body.decode('utf-8'))
        ordered_ids = data.get('order', []) # Expecting {'order': ['uuid1', 'uuid2', ...]}

        if not isinstance(ordered_ids, list):
             raise ValueError("Invalid data format: 'order' must be a list.")

        # Create a mapping of id to its new order
        id_order_map = {category_id: index for index, category_id in enumerate(ordered_ids)}

        # Verify all IDs belong to the current user and exist
        categories_to_update = Category.objects.filter(
            user=request.user,
            id__in=ordered_ids
        )

        if len(categories_to_update) != len(ordered_ids):
            # Find missing/unowned IDs for better error message if needed
            found_ids = {str(cat.id) for cat in categories_to_update}
            missing_ids = [cat_id for cat_id in ordered_ids if cat_id not in found_ids]
            print(f"Warning: User {request.user.id} attempted to reorder non-existent or unowned categories: {missing_ids}")
            # Decide whether to proceed with the ones found or return error
            # For simplicity here, we'll proceed with valid ones, but an error might be safer
            # return JsonResponse({'status': 'error', 'message': f'Invalid or unowned category IDs provided: {missing_ids}'}, status=400)

        # Update the order for each category
        updated_count = 0
        for category in categories_to_update:
            new_order = id_order_map.get(str(category.id)) # Ensure comparison is string vs string if needed
            if new_order is not None and category.order != new_order:
                category.order = new_order
                category.save(update_fields=['order'])
                updated_count += 1

        print(f"Reordered {updated_count} categories for user {request.user.id}")
        return JsonResponse({'status': 'success', 'message': f'{updated_count} categories reordered.'})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception as e:
        # Log the exception for debugging
        print(f"Error reordering categories for user {request.user.id}: {e}")
        return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred.'}, status=500)

@login_required(login_url='login')
def budgets(request):
    user = request.user
    budgets =  Budget.objects.filter(user=user)
    total_limit = budgets.aggregate(Sum('limit'))['limit__sum'] or 0
    total_expense = budgets.aggregate(Sum('expense'))['expense__sum'] or 0

    categories = Category.objects.filter(user=user).order_by('order')
    template_data = {'title': 'Budgets'}
    return render(request, 'finances/budgets.html', {
        'template_data': template_data, 'categories': categories,
        'total_limit': total_limit, 'total_expense': total_expense,})

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
def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)

    if request.method == "POST":
        budget.delete()
        return redirect('finances.budgets')

@login_required(login_url='login')
def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    template_data = {'title': 'Edit Budget'}


    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget, error_class=CustomErrorList)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('finances.budgets')
        template_data['form'] = form
    else:
        template_data['form'] = BudgetForm(instance=budget)

    return render(request, 'finances/budgetEditForm.html',
                  {'template_data': template_data, 'budget': budget})

@login_required(login_url='login')
def transactions(request):
    user = request.user
    categories = Category.objects.filter(user=user).order_by('order')  # Add order_by here
    template_data = {'title': 'Transactions'}
    return render(request, 'finances/transactions.html', {
        'template_data': template_data, 'categories': categories})

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
def reports(request):
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
    
    # Get weekly spending data
    weekly_spending = {}
    current_date = start_date
    while current_date <= end_date:
        # Calculate the start of the week (Monday)
        week_start = current_date - timedelta(days=current_date.weekday())
        week_end = week_start + timedelta(days=6)
        
        # Get the week's total spending
        amount = transactions.filter(
            date__range=[week_start, week_end],
            isExpense=True
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Use the week start date as the key
        week_key = week_start.strftime('%Y-%m-%d')
        weekly_spending[week_key] = amount
        
        # Move to next week
        current_date = week_end + timedelta(days=1)
    
    # Get monthly spending data
    monthly_spending = {}
    current_date = start_date
    while current_date <= end_date:
        month_key = current_date.strftime('%Y-%m')
        amount = transactions.filter(
            date__year=current_date.year,
            date__month=current_date.month,
            isExpense=True
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_spending[month_key] = amount
        current_date += timedelta(days=32)  # Move to next month
    
    context = {
        'template_data': {'title': 'Financial Reports'},
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': total_income - total_expenses,
        'category_expenses': category_expenses,
        'weekly_spending': json.dumps(weekly_spending),
        'monthly_spending': json.dumps(monthly_spending),
    }
    
    return render(request, 'finances/reports.html', context)
