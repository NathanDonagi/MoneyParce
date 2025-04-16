from django.contrib import admin

from finances.models import Budget, Transaction

admin.site.register(Budget)
admin.site.register(Transaction)