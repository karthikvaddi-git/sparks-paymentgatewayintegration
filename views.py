from django.shortcuts import render
from decouple import config
from .models import savenature
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import razorpay
def index(request):
    print(config('RAZOR_KEY_ID'))
    config('RAZOR_KEY_SECRET')

    return render(request,"index.html")

def pay(request):
    if request.method=="POST":
        phone=request.POST.get('phonenumber')

        name=request.POST.get('nameid')
        email=request.POST.get('emailid')
        amount=request.POST.get('amountid')
        amount=int(amount)*100



        client = razorpay.Client(auth=(config('RAZOR_KEY_ID'), config('RAZOR_KEY_SECRET')))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        print(payment)



        saveobj = savenature(name=name, email=email, paymentid=payment['id'],amount=amount,phonenumber=phone)
        saveobj.save()
        context={'payment':payment}

        return render(request, "pay.html",{'payment':payment,'saveobj':saveobj})

    else:
        return render(request,"pay.html")


@csrf_exempt
def success(request):
    if request.method == "POST":


        print(request.POST)
        orderid=request.POST['razorpay_order_id']
        paymentid=request.POST['razorpay_payment_id']
        siganture=request.POST['razorpay_signature']



        client = razorpay.Client(auth=(config('RAZOR_KEY_ID'), config('RAZOR_KEY_SECRET')))
        params_dict = {
            'razorpay_order_id': orderid,
            'razorpay_payment_id': paymentid ,
            'razorpay_signature': siganture
        }



        try:

                status = client.utility.verify_payment_signature(params_dict)
                user = savenature.objects.filter(paymentid=orderid).first()
                user.paid = True
                user.save()
                return HttpResponse("payemnet succesful")


        except:


                # if there is an error while capturing payment.
                return HttpResponse(" arey paymentfail.html")
        else:

            return render(request,"success.html")







def rz(request):
    return render(request,"rz.html")



