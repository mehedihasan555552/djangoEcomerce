from django.shortcuts import render,redirect
from . models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart,guestOrder,cartData


from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import  DetailView

from django.core.paginator import Paginator


# Create your views here.
def Store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']



    products = Product.objects.all()

    paginator = Paginator(products,12)
    page_number = request.GET.get('page',1)
    products=paginator.get_page(page_number)

    context = {'products':products,'cartItems':cartItems,'paginator':paginator,'page_number':page_number}
    return render(request,'store/store.html',context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']



    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)


def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:',productId)

    customer =request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)




def Men(request):
	category=['1']

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.filter(category=category)

	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def Women(request):
	category=['2']

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.filter(category=category)

	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def Kids(request):
	category=['3']

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.filter(category=category)

	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def Electronic(request):
	category=['4']

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.filter(category=category)

	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def Mobile(request):
	category=['5']

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.filter(category=category)

	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def Sports(request):
	category=['6']

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.filter(category=category)

	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def Search(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	query = request.GET['query']
	name = Product.objects.filter(name__icontains=query)
	description = Product.objects.filter(description__icontains=query)
	products = name.union(description)
	context = {'products':products, 'cartItems':cartItems}
	return render(request,'store/search.html', context)





def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + username)
            return redirect('store')
    context={'form':form}
    return render(request,'store/register.html',context)



def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('store')

        else:
            messages.info(request,'username or password incorrect.')
    context={}
    return render(request, 'store/login.html',context)



def userlogout(request):
    logout(request)
    return redirect('store')


class PostDetailView(DetailView):
    model = Product


def Productdetails(request,pk):

	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.get(pk=pk)
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/product_detail.html', context)
