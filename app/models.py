from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]

    TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.type} - {self.amount} - {self.status}'