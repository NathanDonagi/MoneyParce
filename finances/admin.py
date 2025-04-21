from django.contrib import admin

from finances.models import Category, Budget, Transaction

admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Transaction)
