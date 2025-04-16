from django.urls import path
from . import views
urlpatterns = [
    path('profile/', views.profile, name='finances.profile'),
    path('budgets/', views.budgets, name='finances.budgets'),
    path('transactions/', views.transactions, name='finances.transactions'),
    path('progress/', views.progress, name='finances.progress'),
    path('advice/', views.advice, name='finances.advice'),
]