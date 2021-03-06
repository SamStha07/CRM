from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from .models import *
from .forms import OrderForm, CustomerForm
from .filters import OrderFilter

# Create your views here.


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/home.html', context)


def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)


def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter()

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'myFilter': myFilter,
    }
    return render(request, 'accounts/customer.html', context)


def create_order(request, pk):
    orderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = orderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})  #initial will add customer on the form with its prefill customer name

    if request.method == 'POST':
        # print(request.POST)
        # form = OrderForm(request.POST)
        formset = orderFormSet(request.POST, instance=customer)

        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {
        'customer': customer,
        'formset': formset,
    }
    return render(request, 'accounts/order_form.html', context)


def create_customer(request):
    form = CustomerForm()
    if(request.method == 'POST'):
        # print(request.POST)
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'accounts/create_customer.html', context)


def update_order(request, pk):
    order = Order.objects.get(id=pk)
    # instance will prefill the data which is already there
    form = OrderForm(instance=order)

    if(request.method == 'POST'):
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'accounts/order_form.html', context)


def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'order': order
    }
    return render(request, 'accounts/delete_order.html', context)
