from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=6, null=True)
    email = models.EmailField(max_length=30, unique=True)
    total_money = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    daily_spending_limit = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    
    def __str__(self):
        return self.email

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    PAYMENT_DESC = [
        ('meal', 'Meal'),
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('groceries', 'Groceries'),
        ('transportation', 'Transportation'),
        ('insurance', 'Insurance'),
        ('healthcare', 'Healthcare'),
        ('entertainment', 'Entertainment'),
        ('education', 'Education'),
        ('savings', 'Savings'),
        ('debt_repayment', 'Debt Repayment'),
        ('clothing', 'Clothing'),
        ('personal_care', 'Personal Care'),
        ('pets', 'Pets'),
        ('subscriptions', 'Subscriptions'),
        ('miscellaneous', 'Miscellaneous'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='PENDING')
    timestamp = models.DateTimeField(auto_now_add=True) 
    upiId = models.EmailField(max_length=30,null=True)
    description = models.CharField(max_length=255, choices=PAYMENT_DESC, default="miscellaneous")
    remain_daily_target_amt = models.IntegerField(default=0)
    cash_payment = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Payment {self.id} - {self.user.username}'

class CommonExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)