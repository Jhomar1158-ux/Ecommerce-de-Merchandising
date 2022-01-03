from django.http.response import HttpResponse
from django.shortcuts import redirect,HttpResponse, render
from app1.models import *
from django.contrib import messages
from django.core import serializers

import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


def index(request):
    if 'login' not in request.session:
        request.session['login'] = False
    
    if 'u_id' not in request.session:
        request.session['u_id'] = 0
    context={
        'products':Product.objects.all()
    }
    return render(request, "index.html", context)


# ====================PROBANDO EL SEARCH CON SESSION===============================
# def index(request):
#     if 'login' not in request.session:
#         request.session['login'] = False
    
#     if 'u_id' not in request.session:
#         request.session['u_id'] = 0
    
#     if 'result' in request.session:
#         context={
#             'products':request.session['result']
#         }
#         print('*'*10)
#         print(context['products'])
#         print('*'*10)
#     else:
#         context={
#             'products':Product.objects.all()
#         }
#     return render(request, "index.html", context)

# LOGIN AND REGISTER

def register_template(request):
    return render(request, "register.html")




def registro_process(request):
    check = Users.objects.filter(email = request.POST['email'])
    error = False
    
    if len(request.POST['name'])< 3:
        messages.error(request,'Tu nombre debe tener al menos 3 carácteres.', extra_tags = 'fn_error' )
        error = True

    if len(request.POST['apellido'])< 3:
        messages.error(request,'Tu apellido debe tener al menos 3 carácteres.', extra_tags = 'ln_error')
        error = True
    
    if check:
        messages.error(request,'Este email ya se encuentra registrado', extra_tags = 'email_error')
        error = True

    # PASSWORD, CONFIRM PASSWORD 

    if request.POST['password'] != request.POST['confirm_password']:
        messages.error(request,'Las contraseñas no coinciden', extra_tags = 'pw_error')
        error = True

    if len(request.POST['password']) < 8 :
        messages.error(request,'Tu contraseña debe teener al menos 8 carácteres', extra_tags = 'pw_error')
        error = True

    # =======================================

    if error == True:
        return redirect('/register')

    elif error == False:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = Users.objects.create(name = request.POST['name'], lastname = request.POST['apellido'],email=request.POST['email'], default_shipping_address=request.POST['direccion'], password = pw_hash, department=request.POST['selectDepartamento'])
        print(new_user)
        request.session['user_id'] = new_user.id
        return redirect("/login")

def login_template(request):
    return render(request, "login.html")


def login_process(request):
    email = request.POST["email"]
    password = request.POST["password"]
    print(f"{email} {password}")
    echeck = Users.objects.filter(email=email) 
    print (echeck)
    if echeck:
        print('EXISTE EMAIL')
        if bcrypt.checkpw(password.encode(), echeck[0].password.encode()):
            print(echeck[0].password)
            request.session['login'] = True
            request.session['u_id'] = echeck[0].id
            # =======================MODIFICANDO=========================
            return redirect('/home')
        else:
            print('CONTRASEÑA INCORRECTA')
            messages.error(request,'Contraseña incorrecta', extra_tags = 'mal_login_pass_dato')
            return redirect('/login')
    else: 
        messages.error(request,'Email No registrado', extra_tags = 'mal_dato_login_e')
        return redirect('/login')

# ====================== HOME ====================

def home(request):
    print('INGRESO AL DASHBOARD FRIENDS')
    if request.session['login'] == True:
        user_1 = Users.objects.get(id = request.session['u_id'])
        context={
            'products':Product.objects.all(),
            'user': user_1,
        }
        return render(request, 'home.html', context)
    else:
        return redirect('/')


# def secret(request):
#     return render(request,'carousel_secret.html')





# ========== SEarch==========
def search(request):
    var_search=request.POST['search']
    # Quiero que me des los resultados de este nombre a partir de las letras de var_search
    var_result=Product.objects.filter(nombre__contains=var_search)
    print(var_result)
    context={
        'products':var_result
    }
    return render(request, 'index.html',context)





# Probar #2
# POST AND var==name
# Usar un def se search ->








# def search(request):
#     var_search="Polo"
#     # Quiero que me des los resultados de este nombre a partir de las letras de var_search
#     var_result=Product.objects.filter(nombre__contains=var_search)
#     print(var_result)
#     # final_result=[]
#     # for i in var_result:
#     #     final_result.append(i)
#     if 'result' in request.session:
#         del request.session['result']
#     request.session['result']=serializers.serialize('json',[ var_result, ])
#     print('*'*10)
#     print(request.session['result'])
#     return redirect('/')


# ===========LOGOUT============
def logout(request):
    request.session.clear()
    return redirect('/')



# CARRITO DE COMPRAS
# def addToCard(request, id):
#     obj_id_user=Users.objects.get(id=1)
#     obj_order=Orders.objects.filter(user_id=obj_id_user)
#     order=''
#     for i in obj_order:
#         if i.order_status == 'incomplete':
#             order=i
#             break
#     obj_order_details=Order_details.objects.filter(order_id=order)
#     obj_product_id=Product.objects.get(id=id)

#     for i in obj_order_details:
#         if i.product_id == obj_product_id:
#             i.quantity+=1
#             i.save()
#             break
#     print(i.quantity)
#     print(obj_order_details)
#     return redirect('/')

def addToCard(request, id):
    list_product=[]
    producto=Product.objects.get(id=id)
    if list_product:
        list_product.append(producto)
    print(list_product)
    if producto:
        if request.session.get('product_car') == None:
            request.session['product_car']=0
        print('--append--')
        request.session['product_car']+=1

    # REVISAR APPEND
    # print(producto)
    
    # context={
    #     'product_choose': Product.objects.get(id=id),
    #     'products':Product.objects.all(),
    # }
    # return render(request,'productDetails.html',context)


    return redirect(f'/productDetails/{id}')

    

# # Create your views here.
# def search(request):
#     for i in obj_products_all:
#         if key in i.name:
#             print(i.nombre)
#             return render(request,'ProductDetail.html')


# DETALLES DE LOS PRODUCTOS

def productDetails(request, id):
    context={
        'product_choose': Product.objects.get(id=id),
        'products': Product.objects.all(),
    }
    
    return render(request, 'productDetails.html', context)