# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.utils import timezone
# from django.core.mail import send_mail
# from django.conf import settings
# from expenses.forms import CommonExpenseForm
# from .models import Payment, User, CommonExpense
# from .tasks import send_email_task

# def initiate_payment(request):
#     if request.method == "GET":
#         print(timezone.now().date())
#         return render(request, "expenses/initiate_payment.html")
    
#     if request.method == 'POST':
#         print("POST method called !!")
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         daily_limit = request.POST.get('daily_limit')
#         amount = int(request.POST.get('amount'))

#         if not username or not email or not amount:
#             return render(request, 'expenses/initiate_payment.html', {'error': 'Username, email, and amount are required.'})
        
#         try:
#             user = User.objects.get(username__iexact=username, email=email)
#         except User.DoesNotExist:
#             user = User.objects.create(username=username, email=email, daily_spending_limit=daily_limit)
#         print("user", user)
#         total_amt = user.total_money
        
#         if total_amt > amount:
#             payment = Payment.objects.create(user=user, amount=amount, status='PENDING')
#         else:
#             return render(request, 'expenses/initiate_payment.html', {'error':'You do not have sufficient balance'})
        
#         return redirect('process_payment', payment_id=payment.id)
    
#     return render(request, 'expenses/initiate_payment.html')

# def process_payment(request, payment_id):
#     payment = Payment.objects.get(id=payment_id)
#     payment.status = 'COMPLETED'
#     payment.save()
#     print('payment :', payment)
#     amt = payment.amount
#     u*ser = payment.user
#     user.total_money -= amt
#     user.save()
    
#     subject = 'Payment Confirmation'
#     message = f'Thank you for your payment of ${payment.amount}. Your payment has been processed successfully.'
#     from_email = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [payment.user.email]

#     # Call the Celery task
#     # send_email_task.delay(subject, message, from_email, recipient_list)

#     return render(request, 'expenses/payment_success.html', {'payment': payment})

# # # def send_email_view(request):
# # #     subject = 'Test Email'
# # #     message = 'This is a test email sent from Celery.'
# # #     # from_email = 'pratikshashikhare4016@gmail.com'
# # #     # recipient_list = ['pratiksha9200@gmail.com']
# # #     from_email = settings.DEFAULT_FROM_EMAIL
# # #     recipient_list = ['pratiksha9200@gmail.com']

# # #     # Call the Celery task
# # #     send_email_task.delay(subject, message, from_email, recipient_list)

# # #     return HttpResponse('Email sent!')


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings

from .forms import CommonExpenseForm
from .models import Payment, User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User,CommonExpense,Payment

@login_required
def initiate_payment(request):
    if request.method == "GET":
        user = request.session.get('user_id')
        print(user)
        exp = CommonExpense.objects.filter(user=user)
        total_monthly_exp = 0
        for i in exp:
            total_monthly_exp += i.amount
        print(total_monthly_exp)
        bal = User.objects.get(id=user)
        bal = bal.total_money
        bal = int(bal) - int(total_monthly_exp)
        return render(request, "expenses/initiate_payment.html", {'usable_balance':bal, 'exp':exp, 'total_monthly_exp':total_monthly_exp})

    if request.method == 'POST':
        userId = request.session.get('user_id')
        user = User.objects.get(id=userId)
        username = user.username
        email = user.email
        daily_limit = request.POST.get('daily_limit')
        amount = int(request.POST.get('amount',0))
        if not username or not email or not amount:
            return render(request, 'expenses/initiate_payment.html', {'error': 'Username, email, and amount are required.'})
        try:
            user = User.objects.get(username__iexact=username, email=email)
            user.daily_spending_limit = int(daily_limit)
            user.save()
            
        except User.DoesNotExist:
            user = User.objects.create(username=username, email=email, daily_spending_limit=daily_limit)
        
        today = timezone.now().date()
        payments_today = Payment.objects.filter(user=user, timestamp__date=today)
        total_spent_today = sum(payment.amount for payment in payments_today)

        if total_spent_today + amount > user.daily_spending_limit:
            return render(request, 'expenses/initiate_payment.html', {'error': 'You crossed the daily target of amount spending'})
                
        if user.total_money >= amount:
            payment = Payment.objects.create(user=user, amount=amount, status='PENDING')
            return redirect('process_payment', payment_id=payment.id)
        else:
            return render(request, 'expenses/initiate_payment.html', {'error': 'You do not have sufficient balance'})

    return render(request, 'expenses/initiate_payment.html')

def process_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    payment.status = 'COMPLETED'
    payment.save()

    # Deduct the payment amount from the user's total money
    user = payment.user
    user.total_money -= payment.amount
    user.save()
    
    # Send payment confirmation email
    subject = 'Payment Confirmation'
    message = f'Thank you for your payment of ${payment.amount}. Your payment has been processed successfully.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Call the Celery task to send email asynchronously
    # send_email_task.delay(subject, message, from_email, recipient_list)

    return render(request, 'expenses/payment_success.html', {'payment': payment})

def add_common_expense(request):
    if request.method == 'POST':
        form = CommonExpenseForm(request.POST)
        if form.is_valid():
            common_expense = form.save(commit=False)
            common_expense.user = form.cleaned_data['user']
            common_expense.save()
            return redirect('initiate_payment')
    else:
        form = CommonExpenseForm()
    return render(request, 'expenses/add_common_expense.html', {'form': form})

def signup(request):
    if request.method == 'GET':
        return render(request, 'expenses/signup.html')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if user with the same email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return redirect('signup')

        # Create new user
        user = User.objects.create(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'expenses/login.html')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email, password=password).first()
        if user:
            request.session['user_id'] = user.id
            messages.success(request, 'Logged in successfully.')
            return redirect('initiate_payment')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    request.session.clear()
    messages.success(request, 'Logged out successfully.')
    return redirect('login')
