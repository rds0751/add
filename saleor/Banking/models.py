from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User

class Transaction(models.Model):
    marketing_plan = models.CharField(max_length=50, choices=settings.TREE_TYPES)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, unique=False, related_name='user_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, unique=False, related_name='user_receiver', on_delete=models.CASCADE)
    date = models.DateTimeField()
    amount = models.FloatField()
    
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('marketing_plan', 'date', 'sender', 'receiver', 'amount',)

admin.site.register(Transaction, TransactionAdmin)