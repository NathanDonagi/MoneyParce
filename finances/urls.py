from django.urls import path
from . import views
urlpatterns = [
    path('profile/', views.profile, name='finances.profile'),
    path('budgets/', views.budgets, name='finances.budgets'),
    path('budgets/form', views.budgets_form, name='finances.budgets_form'),
    path('transactions/', views.transactions, name='finances.transactions'),
    path('transactions/form', views.transactions_form, name='finances.transactions_form'),
    path('transactions/delete/<uuid:transaction_id>/', views.delete_transaction, name='finances.delete_transaction'),
    path('transactions/edit/<uuid:transaction_id>/', views.edit_transaction, name='finances.edit_transaction'),
    path('progress/', views.progress, name='finances.progress'),
    path('ask/', views.gemini_help, name='gemini_help'),
]