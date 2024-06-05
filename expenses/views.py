from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from expenses.forms import CommonExpenseForm
from .models import Payment, User, CommonExpense
from django.http import HttpResponse
from .tasks import send_email_task
from django.contrib import messages

# # def initiate_payment(request):
# #     if request.method == "GET":
# #         print(timezone.now().date())
# #         return render(request, "expenses/initiate_payment.html")
    
# #     if request.method == 'POST':
# #         print("POST method called !!")
# #         username = request.POST.get('username')
# #         email = request.POST.get('email')
# #         daily_limit = request.POST.get('daily_limit')
# #         amount = int(request.POST.get('amount'))

# #         if not username or not email or not amount:
# #             return render(request, 'expenses/initiate_payment.html', {'error': 'Username, email, and amount are required.'})
        
# #         try:
# #             user = User.objects.get(username__iexact=username, email=email)
# #         except User.DoesNotExist:
# #             user = User.objects.create(username=username, email=email, daily_spending_limit=daily_limit)
# #         print("user", user)
# #         total_amt = user.total_money
        
# #         if total_amt > amount:
# #             payment = Payment.objects.create(user=user, amount=amount, status='PENDING')
# #         else:
# #             return render(request, 'expenses/initiate_payment.html', {'error':'You do not have sufficient balance'})
        
# #         return redirect('process_payment', payment_id=payment.id)
    
# #     return render(request, 'expenses/initiate_payment.html')

# # def process_payment(request, payment_id):
# #     payment = Payment.objects.get(id=payment_id)
# #     payment.status = 'COMPLETED'
# #     payment.save()
# #     print('payment :', payment)
# #     amt = payment.amount
# #     u*ser = payment.user
# #     user.total_money -= amt
# #     user.save()
    
# #     subject = 'Payment Confirmation'
# #     message = f'Thank you for your payment of ${payment.amount}. Your payment has been processed successfully.'
# #     from_email = settings.DEFAULT_FROM_EMAIL
# #     recipient_list = [payment.user.email]

# #     # Call the Celery task
# #     # send_email_task.delay(subject, message, from_email, recipient_list)

# #     return render(request, 'expenses/payment_success.html', {'payment': payment})

# # # # def send_email_view(request):
# # # #     subject = 'Test Email'
# # # #     message = 'This is a test email sent from Celery.'
# # # #     # from_email = 'pratikshashikhare4016@gmail.com'
# # # #     # recipient_list = ['pratiksha9200@gmail.com']
# # # #     from_email = settings.DEFAULT_FROM_EMAIL
# # # #     recipient_list = ['pratiksha9200@gmail.com']

# # # #     # Call the Celery task
# # # #     send_email_task.delay(subject, message, from_email, recipient_list)

# # # #     return HttpResponse('Email sent!')


# from django.shortcuts import render, redirect
# from django.utils import timezone
# from datetime import timedelta
# from .forms import CommonExpenseForm
# from .models import Payment, User, CommonExpense
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.mail import send_mail

# @login_required
# def initiate_payment(request):
#     if request.method == "GET":
#         user = request.session.get('user_id')
#         us = User.objects.get(id=user)
#         daily_max_spending_amt = us.daily_spending_limit
#         p = Payment.objects.filter(user=user).order_by('timestamp').last()
#         if p:
#             remain_daily_target_amt = p.remain_daily_target_amt
#         else:
#             remain_daily_target_amt = 100
#         email = us.email
#         exp = CommonExpense.objects.filter(user=user)
#         total_monthly_exp = 0
#         for i in exp:
#             total_monthly_exp += i.amount
#         # bal = User.objects.get(id=user)
#         bal = us.total_money
#         usable_bal = int(bal) - int(total_monthly_exp)
#         current_date_time = timezone.now()
#         last_month_datetime = current_date_time - timedelta(days=current_date_time.day)
#         last_month_num = last_month_datetime.month

#         record = Payment.objects.filter(user=user, timestamp__month=last_month_num)
#         print("record", record)
        
#         yesterday = current_date_time - timedelta(days=1)
#         # prev_pay = Payment.objects.filter(id=user,  timestamp__date=yesterday)
#         prev_pay = Payment.objects.filter(timestamp__date=yesterday)
#         print(prev_pay)
#         prev_amt = 0
#         for p in prev_pay:
#             prev_amt += p.amount
#         print("prev_amt", prev_amt)
#         print("Yesterday's date:", yesterday.date())
#         return render(request, "expenses/initiate_payment.html", 
#                       {'usable_balance':usable_bal, 
#                        'exp':exp, 
#                        'total_monthly_exp':total_monthly_exp, 
#                        "remain_daily_target_amt":remain_daily_target_amt,
#                        "daily_max_spending_amt": daily_max_spending_amt,
#                        "total_acc_bal": bal,
#                        })

#     if request.method == 'POST':
#         userId = request.session.get('user_id')
#         user = User.objects.get(id=userId)
#         username = user.username
#         email = user.email
#         daily_limit = request.POST.get('daily_limit')
#         amount = int(request.POST.get('amount',0))
#         upiId = request.POST.get("wemail")
#         desc = request.POST.get("desc")

#         try:
#             user = User.objects.get(username__iexact=username, email=email)
#             user.daily_spending_limit = int(daily_limit)
#             user.save()
            
#         except User.DoesNotExist:
#             user = User.objects.create(username=username, email=email, daily_spending_limit=daily_limit, upiId=upiId, description=desc)
        
#         today = timezone.now().date()
#         payments_today = Payment.objects.filter(user=user, timestamp__date=today)
#         total_spent_today = sum(payment.amount for payment in payments_today)
#         spending_amt = total_spent_today + amount

#         if spending_amt > user.daily_spending_limit:
#             send_mail(
#             'Oops! Target is Crossing',
#             'You are crossing the daily max spending target. Today you spend {total_spent_today}. If you want to continue increasse you daily target',
#             'pratiksha9200@gmail.com',
#             ['4016pinki@gmail.com', email],
#             fail_silently=False,
#         )
#             return render(request, 'expenses/initiate_payment.html', {'error': 'You crossing the daily target of amount spending'})
        
#         elif user.total_money >= amount <= spending_amt:
#             payment = Payment.objects.create(user=user, amount=amount, status='COMPLETED')

#             user = payment.user
#             user.total_money -= payment.amount
#             payment.remain_daily_target_amt -= payment.amount
#             user.save()
#             payment.save()

#             send_mail(
#             'Payment',
#             'You did the payment of ₹ {amount}.',
#             'pratiksha9200@gmail.com',
#             ['4016pinki@gmail.com', email],
#             fail_silently=False,
#         )
#             return redirect('process_payment', payment_id=payment.id)
#         else:
#             return render(request, 'expenses/initiate_payment.html', {'error': 'You do not have sufficient balance'})


#     return render(request, 'expenses/initiate_payment.html')

# def process_payment(request, payment_id):
#     payment = Payment.objects.get(id=payment_id)
#     return render(request, 'expenses/payment_success.html', {'payment': payment})

# def add_common_expense(request):
#     if request.method == 'POST':
#         form = CommonExpenseForm(request.POST)
#         if form.is_valid():
#             common_expense = form.save(commit=False)
#             common_expense.user = form.cleaned_data['user']
#             common_expense.save()
#             return redirect('initiate_payment')
#     else:
#         form = CommonExpenseForm()
#     return render(request, 'expenses/add_common_expense.html', {'form': form})

# def signup(request):
#     if request.method == 'GET':
#         return render(request, 'expenses/signup.html')
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         # Check if user with the same email already exists
#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email is already taken.')
#             return redirect('signup')

#         # Create new user
#         user = User.objects.create(username=username, email=email, password=password)
#         messages.success(request, 'Account created successfully. Please login.')
#         return redirect('login')
#     else:
#         return render(request, 'signup.html')

# def login(request):
#     if request.method == 'GET':
#         return render(request, 'expenses/login.html')

#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']

#         user = User.objects.filter(email=email, password=password).first()
#         if user:
#             request.session['user_id'] = user.id
#             messages.success(request, 'Logged in successfully.')
#             return redirect('initiate_payment')
#         else:
#             messages.error(request, 'Invalid credentials. Please try again.')
#             return redirect('login')
#     else:
#         return render(request, 'login.html')

# def logout(request):
#     request.session.clear()
#     messages.success(request, 'Logged out successfully.')
#     return redirect('login')

# # def send_email_view(request):
# #     subject = 'Test Email'
# #     message = 'This is a test email sent from Celery.'
# #     # from_email = 'pratikshashikhare4016@gmail.com'
# #     # recipient_list = ['pratiksha9200@gmail.com']
# #     from_email = settings.DEFAULT_FROM_EMAIL
# #     recipient_list = ['pratiksha9200@gmail.com']

# #     # Call the Celery task
# #     # send_email_task.delay(subject, message, from_email, recipient_list)

# #     return HttpResponse('Email sent!')
# # from django.core.mail import send_mail

# # send_mail(
# #     'Subject here',
# #     'Here is the message.',
# #     'pratiksha9200@gmail.com',
# #     ['4016pinki@gmail.com'],
# #     fail_silently=False,
# # )


from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from .models import User, Payment, CommonExpense

def landing(request):
    return render(request, 'expenses/landing.html')

def get_payment_context(user):
    daily_max_spending_amt = user.daily_spending_limit
    p = Payment.objects.filter(user=user).order_by('timestamp').last()    
        
    exp = CommonExpense.objects.filter(user=user)
    total_monthly_exp = sum(e.amount for e in exp)

    bal = user.total_money
    usable_bal = int(bal) - int(total_monthly_exp)

    current_date_time = timezone.now()
    last_month_datetime = current_date_time - timedelta(days=current_date_time.day)
    last_month_num = last_month_datetime.month

    record = Payment.objects.filter(user=user, timestamp__month=last_month_num)
    last_month_total_spend = 0
    last_month_saved_amt = 0
    if record:
        for payment in record:
            last_month_total_spend += payment.amount
        last_month_saved_amt = bal - last_month_saved_amt
    
    yesterday = current_date_time - timedelta(days=1)
    prev_pay = Payment.objects.filter(user=user, timestamp__date=yesterday)
    
    p = Payment.objects.filter(user=user, timestamp__date=yesterday).order_by('timestamp').last()
    yesterdays_saving = p.remain_daily_target_amt
    yesterdays_max_target = user.daily_spending_limit
    
    prev_amt = sum(p.amount for p in prev_pay)
    today = timezone.now().date()
    payments_today = Payment.objects.filter(user=user, timestamp__date=today)
    total_spent_today = sum(payment.amount for payment in payments_today)
    
    remain_daily_target_amt = daily_max_spending_amt - total_spent_today
    
    cash_pay = Payment.objects.filter(user=user, timestamp__date=today, cash_payment=True)
    today_cash_spend = 0
    for cash_amt in cash_pay:
        today_cash_spend += cash_amt.amount

    online_pay = Payment.objects.filter(user=user, timestamp__date=today, cash_payment=False)
    today_online_spend = 0
    for online_amt in online_pay:
        today_online_spend += online_amt.amount

    context = {
        'usable_balance': usable_bal,
        'exp': exp,
        'total_monthly_exp': total_monthly_exp,
        'remain_daily_target_amt': remain_daily_target_amt,
        'daily_max_spending_amt': daily_max_spending_amt,
        'total_acc_bal': bal,
        'total_spent_today': total_spent_today,
        'yesterday_spend_amt': prev_amt,
        "last_month_spend_amt": last_month_total_spend,
        "last_month_saved_amt": last_month_saved_amt,
        "today_cash_spend": today_cash_spend,
        "today_online_spend": today_online_spend,
        "yesterdays_saving": yesterdays_saving,
        "yesterdays_max_target": yesterdays_max_target,
    }
    return context

def initiate_payment(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)

    if request.method == "GET":
        context = get_payment_context(user)
        return render(request, "expenses/initiate_payment.html", context)

    if request.method == 'POST':
        daily_limit = request.POST.get('daily_limit')
        amount = int(request.POST.get('amount', 0))
        upiId = request.POST.get("wemail")
        desc = request.POST.get("desc")

        user.daily_spending_limit = int(daily_limit)
        user.save()

        today = timezone.now().date()
        payments_today = Payment.objects.filter(user=user, timestamp__date=today)
        total_spent_today = sum(payment.amount for payment in payments_today)
        spending_amt = total_spent_today + amount

        if spending_amt > user.daily_spending_limit:
            send_mail(
                'Oops! Target is Crossing',
                f'You are crossing the daily max spending target. Today you spent {total_spent_today}. If you want to continue, increase your daily target.',
                'pratiksha9200@gmail.com',
                ['4016pinki@gmail.com', user.email],
                fail_silently=False,
            )
            context = get_payment_context(user)
            context['error'] = 'You are crossing the daily target amount of spending.'
            return render(request, 'expenses/initiate_payment.html', context)

        if user.total_money >= amount <= spending_amt:
            payment = Payment.objects.create(user=user, amount=amount, status='COMPLETED', upiId=upiId, description=desc)

            user.total_money -= payment.amount
            payment.remain_daily_target_amt = (payment.remain_daily_target_amt or user.daily_spending_limit) - payment.amount
            user.save()
            payment.save()

            send_mail(
                'Payment',
                f'You made a payment of ₹ {amount}.',
                'pratiksha9200@gmail.com',
                ['4016pinki@gmail.com', user.email],
                fail_silently=False,
            )
            return redirect('process_payment', payment_id=payment.id)

        context = get_payment_context(user)
        context['error'] = 'You do not have sufficient balance.'
        return render(request, 'expenses/initiate_payment.html', context)

    return render(request, 'expenses/initiate_payment.html')

def process_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    return render(request, 'expenses/payment_success.html', {'payment': payment})

def add_common_expense(request):
    if request.method == 'POST':
        id = request.session.get('user_id')
        user = User.objects.get(id=id)
        # user = request.POST.get('user')
        user = user 
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        if user and amount and description:
            # Create CommonExpense instance and save it
            common_expense = CommonExpense.objects.create(user=user, amount=amount, description=description)
            return redirect('initiate_payment')
        else:
            # Handle form validation errors
            error_message = "All fields are required."
            return render(request, 'expenses/add_common_expense.html', {'error_message': error_message})
    else:
        return render(request, 'expenses/add_common_expense.html')

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

def cash_payment(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        amt = request.POST.get('amount')
        desc = request.POST.get('description')
        Payment.objects.create(user=user, amount=int(amt), status="COMPLETED", description=desc, cash_payment=True)
        # user.total_money -= int(amt)
        # user.save()
        send_mail(
                    'Payment Confirmation',
                    f'You made a cash payment of ₹{amt}.',
                    'pratiksha9200@gmail.com',
                    [user.email, "4016pinki@gmail.com"],
                    fail_silently=False,
                )
        messages.success(request, 'Cash Payment successful.')
        return redirect("initiate_payment")