from django.shortcuts import redirect, render

from app1.models import *

# Create your views here.


def index(request):
    context={
        'products':Product.objects.all()
    }
    return render(request, "index.html", context)

def addToCard(request, id):
    obj_id_user=Users.objects.get(id=1)
    obj_order=Orders.objects.filter(user_id=obj_id_user)
    order=''
    for i in obj_order:
        if i.order_status == 'incomplete':
            order=i
            break
    obj_order_details=Order_details.objects.filter(order_id=order)
    obj_product_id=Product.objects.get(id=id)

    for i in obj_order_details:
        if i.product_id == obj_product_id:
            i.quantity+=1
            i.save()
            break
    print(i.quantity)
    print(obj_order_details)
    return redirect('/')