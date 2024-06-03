from django.contrib import admin
from .models import Payment, User, CommonExpense

# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "amount", "status", "timestamp"]
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email",'total_money','daily_spending_limit']
    
@admin.register(CommonExpense)
class CommonExpAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'description', 'timestamp']