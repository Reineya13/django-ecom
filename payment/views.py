from django.shortcuts import render, redirect
from cart.cart import Cart
from payment import forms
from .models import ShippingAddress, Order, OrderItem
from store.models import Proudct, Profile
from django.contrib import messages
from django.contrib.auth.models import User
import datetime


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order= Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        
        if request.POST:
            status = request.POST['shipping_status']
            if status == "true":
                order= Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped = True, date_shipped = now)
                
                messages.success(request, "Shipping Status Updated")
                return redirect('shipped_dash')
            else:
                order= Order.objects.filter(id=pk)
                order.update(shipped = False)
                
                messages.success(request, "Shipping Status Updated")
                return redirect('not_shipped_dash')
        
        return render(request, 'orders.html',{'order':order, 'items':items}) 
    else:
        messages.success(request, "Acesess Denied")
        return redirect('home')
    
    

def shipped_dash(request):

    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        
        if request.POST:
            status = request.POST['shipping_status']
            id_num = request.POST['num']
            if status == "true":
                order= Order.objects.filter(id=id_num)
                now = datetime.datetime.now()
                order.update(shipped = True, date_shipped = now)
                
                messages.success(request, "Shipping Status Updated")
                return redirect('shipped_dash')
            else:
                order= Order.objects.filter(id=id_num)
                order.update(shipped = False)
                
                messages.success(request, "Shipping Status Updated")
                return redirect('not_shipped_dash')
        
        return render(request, 'shipped_dash.html',{'orders':orders}) 
    else:
        messages.success(request, "Acesess Denied")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            id_num = request.POST['num']
            if status == "true":
                order= Order.objects.filter(id=id_num)
                now = datetime.datetime.now()
                order.update(shipped = True, date_shipped = now)
                
                messages.success(request, "Shipping Status Updated")
                return redirect('shipped_dash')
            else:
                order= Order.objects.filter(id=id_num)
                order.update(shipped = False)
                
                messages.success(request, "Shipping Status Updated")
                return redirect('not_shipped_dash')
        
        return render(request, 'not_shipped_dash.html',{'orders':orders})    
    else:
        messages.success(request, "Acesess Denied")
        return redirect('home')


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        cart_quantites = cart.get_quants
        totals = cart.cart_total()
        
        # get billing info from the last page
        payment_form = forms.PaymentForm(request.POST or None)
       
        # the data of shipping from session 
        my_shipping = request.session.get('my_shipping')
        
        # gather order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # conect address  to one item instead od a dict 
        shipping_address = f"{my_shipping['shipping_address1']}\n {my_shipping['shipping_address2']}\n {my_shipping['shipping_city']}\n {my_shipping['shipping_state']}\n {my_shipping['shipping_zipcode']}\n {my_shipping['shipping_country']}\n"
        amount_paid = totals
        
        if request.user.is_authenticated:
            user = request.user
            # create order logged in
            create_order = Order(user=user,full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            # get order ID
            order_id = create_order.pk
            
            # get product info
            for product in cart_products():
                
             # get product ID's
                product_id = product.id
            # product price
                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price
            # get quants of each prod
                for key, value in cart_quantites().items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id ,user = user, quantity=value, price=product_price)
                        create_order_item.save()    
                
            # remove cart items
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]
                    
            current_user = Profile.objects.filter(user__id = request.user.id)
            # delete shopping cart from db
            current_user.update(old_cart="")
            
            
            messages.success(request, "Order Placed")
            return redirect('home')
            
        else:
            # create order to non logged in
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            order_id = create_order.pk
            
            # get product info
            for product in cart_products():
                
                # get product ID's
                product_id = product.id
                # product price
                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price
                # get quants of each prod
                for key, value in cart_quantites().items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id , quantity=value, price=product_price)
                        create_order_item.save() 
            
            # delete the cart
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]
            
            
            
            messages.success(request,"Order Placed")
            return redirect('home')
            
    else:
        messages.success(request, "Access Denied")
        return redirect('home')



def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        cart_quantites = cart.get_quants
        totals = cart.cart_total()
        
        my_shipping =request.POST
        request.session['my_shipping'] = my_shipping
        
        if request.user.is_authenticated:
            billing_form = forms.PaymentForm()
            return render(request, 'billing_info.html', {'cart_products': cart_products , 'cart_quantites' : cart_quantites, 'totals': totals, 'shipping_info': request.POST, 'billing_form':billing_form})
        else:
            billing_form = forms.PaymentForm()
            return render(request, 'billing_info.html', {'cart_products': cart_products , 'cart_quantites' : cart_quantites, 'totals': totals, 'shipping_info': request.POST, 'billing_form':billing_form})
       
   
    else:
        messages.success(request, "Access Denied")
        return redirect('home')
    
    
    
    
def payment_success(request):
    
    return render(request, 'payment_success.html')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    cart_quantites = cart.get_quants
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        # checkout as logged in user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = forms.ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'checkout.html', {'cart_products': cart_products , 'cart_quantites' : cart_quantites, 'totals': totals, 'shipping_form': shipping_form})
    
    else:
        # checkout as guest
        shipping_form = forms.ShippingForm(request.POST or None)
        return render(request, 'checkout.html', {'cart_products': cart_products , 'cart_quantites' : cart_quantites, 'totals': totals, 'shipping_form': shipping_form})
