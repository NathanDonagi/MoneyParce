from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports, name='financial_reports'),
    path('trends/', views.spending_trends, name='spending_trends'),
] 