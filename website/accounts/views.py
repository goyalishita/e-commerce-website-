from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filters import orderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.models import Group


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):
    c=request.user.customer
    form=CustomerForm(instance=c)
    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=c)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request,'accounts/account_settings.html',context)

@unauthenticated_user
def registerPage(request):
    form=CreateUSerForm()
    if request.method=='POST':
        form=CreateUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
              
            messages.success(request,"Account was created for "+ username)
            return redirect('login')
    context={'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is incorrect')
       context={}
       return render(request,'accounts/login.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userPage(request):
    ord=request.user.customer.order_set.all()
    totord=ord.count()
    delievered=ord.filter(status="Delievered").count()
    pending=ord.filter(status="pending").count()
    context={
    'orders':ord,
    'totord':totord,
    'pending':pending,
    'delievered':delievered }
    return render(request,'accounts/user.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    ord=Order.objects.all()
    cust=Customer.objects.all()
    totcust=cust.count()
    totord=ord.count()
    delievered=ord.filter(status="Delievered").count()
    pending=ord.filter(status="pending").count()
    context={'customers':cust,
    'orders':ord,
    'totord':totord,
    'totcust':totcust,
    'pending':pending,
    'delievered':delievered }
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customers(request,pk_test): 
    cust=Customer.objects.get(id=pk_test)

    ord=cust.order_set.all()
    ord_cnt=ord.count()
    myfilter = orderFilter(request.GET,queryset=ord)
    ord=myfilter.qs
    context= {'customer':cust, 'ord_cnt':ord_cnt,
    'orders':ord,'myfilter':myfilter}
    return render(request,'accounts/customers.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request,pk_test):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('Product','status'),extra=10)
    customer=Customer.objects.get(id=pk_test)
    formset= OrderFormSet(queryset=Order.objects.none() , instance= customer)
    #form = OrderForm(initial={'Customer':customer})
    if(request.method =='POST'):
        #print("printtttttttttttt:",request.POST)
        #form=OrderForm(request.POST)
        formset= OrderFormSet(request.POST,instance= customer)
        if(formset.is_valid()):
            formset.save()
            return redirect('/')

    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    if(request.method =='POST'):
        form=OrderForm(request.POST,instance=order)
        if(form.is_valid()):
            form.save()
            return redirect('/')
    form=OrderForm(instance=order)
    context={'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    if(request.method=='POST'):
        order.delete()
        return redirect('/')

    context={'item':order}
    return render(request,'accounts/delete.html',context)