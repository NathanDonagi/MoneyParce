from django.urls import path
from . import views
urlpatterns = [
    path('profile/', views.profile, name='finances.profile'),
    path('categories/create/', views.create_category, name='finances.create_category'),
    path('categories/delete/<uuid:category_id>/', views.delete_category, name='finances.delete_category'),
    path('categories/rename/<uuid:category_id>/', views.rename_category, name='finances.rename_category'),
    path('categories/reorder/', views.reorder_categories, name='finances.reorder_categories'),
    path('budgets/', views.budgets, name='finances.budgets'),
    path('budgets/form', views.budgets_form, name='finances.budgets_form'),
    path('budgets/delete/<uuid:budget_id>/', views.delete_budget, name='finances.delete_budget'),
    path('budgets/edit/<uuid:budget_id>/', views.edit_budget, name='finances.edit_budget'),
    path('transactions/', views.transactions, name='finances.transactions'),
    path('transactions/form', views.transactions_form, name='finances.transactions_form'),
    path('transactions/delete/<uuid:transaction_id>/', views.delete_transaction, name='finances.delete_transaction'),
    path('transactions/edit/<uuid:transaction_id>/', views.edit_transaction, name='finances.edit_transaction'),
    path('reports/', views.reports, name='finances.reports'),
]