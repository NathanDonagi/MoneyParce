import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from accounts.models import CustomUser

class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='categories')
    order = models.IntegerField(default=0, help_text="Order for sorting categories")

    def __str__(self):
        return self.name


class Budget(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='budgets')
    limit = models.IntegerField()
    expense = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='budgets')

    def __str__(self):
        return self.name

class Transaction(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    description = models.CharField(max_length=255)
    amount = models.FloatField()
    isExpense = models.BooleanField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return self.description
