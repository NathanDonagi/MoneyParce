from django.db import models
from django.contrib.auth.models import User

from accounts.models import CustomUser


class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    limit = models.IntegerField()
    expense = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='budgets')

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    amount = models.IntegerField()
    isExpense = models.BooleanField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return str(self.id) + ' - ' + self.description

