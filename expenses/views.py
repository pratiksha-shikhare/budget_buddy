from django.shortcuts import render, redirect
from .models import Payment
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Payment, User

def initiate_payment(request):
    if request.method == "GET":
        return render(request,"expenses/initiate_payment.html")
    
    if request.method == 'POST':
        print("POST method called !!")
        username = request.POST.get('username')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        print(username, email, amount)

        if not username or not email or not amount:
            return render(request, 'expenses/initiate_payment.html', {'error': 'Username, email, and amount are required.'})
        
        if User.objects.filter(email=email).exists():
            return render(request, "expenses/initiate_payment.html", {'error': 'Email already exist'})
        
        try:
            user = User.objects.get(username__iexact=username, email=email)
            print("same user is fetched", user)
        except User.DoesNotExist:
            user = User.objects.create(username=username, email=email)
        
        payment = Payment.objects.create(user=user, amount=amount, status='PENDING')
        
        return redirect('process_payment', payment_id=payment.id)
    
    return render(request, 'expenses/initiate_payment.html')

def process_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    payment.status = 'COMPLETED'
    payment.save()
    return render(request, 'expenses/payment_success.html', {'payment': payment})
