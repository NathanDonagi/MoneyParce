from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('login/', views.login, name='accounts.login'),
    path('signup/', views.signup, name='accounts.signup'),
    path('reset/', views.reset, name='accounts.reset'),
    path('logout/', views.logout, name='accounts.logout'),
]