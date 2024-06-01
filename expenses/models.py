from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, unique=True)
    
    def __str__(self):
        return self.username

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='PENDING')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment {self.id} - {self.user.username}'
