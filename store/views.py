from django.shortcuts import render, redirect 
from .models import Proudct, Category, Customer, Order, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.db.models import Q
from cart.cart import Cart
from payment import forms
from django.core.paginator import Paginator

from payment.models import ShippingAddress



import json



def all_products(request):
    categories = Category.objects.all()
    products = Proudct.objects.all()
    
    return render(request, 'all_products.html',{'categories': categories, 'products':products})  


def search(request):
    
    if request.method == "POST":
        searched = request.POST['searched']
        prods = Proudct.objects.filter(Q(name__icontains = searched) | Q(description__icontains = searched))
        
        if not searched:
            messages.success(request, "That Product Does Not Exists, Please Try again!")
            return redirect('home')
        else:
            return render(request, 'search.html',{ 'searched':searched, 'prods':prods})
    else:
        return render(request, 'search.html',{})
        
        



def category(request, foo):
    # ... rest of your code ...

    cart = Cart(request)
    cart_prods = cart.get_prods()
    cart_quantites = cart.get_quants()
    totals = cart.cart_total()
    cart_length = cart.__len__()

    if foo == "Sale":
        try:
            products = Proudct.objects.filter(is_sale=True)
            return render(request, 'category.html', {'products': products, 'category': 'Sale', 'cart_prods': cart_prods, 'cart_quantites': cart_quantites, 'cart_totals': totals, 'cart_length': cart_length})
        except:
            messages.success(request, ("No Sale Products Exist"))
            return redirect('home')
    else:
        try:
            category = Category.objects.get(name=foo)
            products = Proudct.objects.filter(category=category)
            return render(request, 'category.html', {'products': products, 'category': category, 'cart_prods': cart_prods, 'cart_quantites': cart_quantites, 'cart_totals': totals, 'cart_length': cart_length})
        except:
            messages.success(request, ("That category doesnt exist"))
            return redirect('home')
        
   
    
def category_summary(request):
    categories = Category.objects.all()
    products = Proudct.objects.all()
    
    return render(request, 'category_summary.html',{'categories': categories, 'products':products})    
    
    
def home(request):
    products = Proudct.objects.all()
    cart = Cart(request)
    cart_prods = cart.get_prods
    cart_quantites = cart.get_quants()
    totals = cart.cart_total()  
    cart_length = cart.__len__()
    
   
    # paginator
    p = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)    
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'products_list_partial.html', {'page_obj': page_obj,'cart_length': cart_length, 'cart_prods':cart_prods, 'cart_quantites':cart_quantites,'cart_totals':totals })
    
    return render(request, 'home.html', {'products': products,'page_obj': page_obj, 'cart_prods':cart_prods,'cart_length':cart_length, 'cart_quantites':cart_quantites, 'cart_totals':totals})



def about(request):
    
    return render(request, 'about.html',{})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                # convert str to dictionary
                coverted_cart = json.loads(saved_cart)
                # add the card to session
                cart = Cart(request)
                for key, value in coverted_cart.items():
                    cart.db_add(product=key, quantity=value)
            
            messages.success(request, ("You have been logged in"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error, please try again"))
            return redirect('login') 
            
    else:
        return render(request, 'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))

    return redirect('home')

def register_user(request):
    form = SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Username created, Let's Add Your Billing Info!"))
            return redirect('update_info')
        else: 
            messages.success(request, ("Whoops!, there was a problem registering please try again!"))
            return redirect('register')
    
    return render(request, 'register.html', {'form':form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        update_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if update_form.is_valid():
            update_form.save()
            
            login(request, current_user)
            messages.success(request, ("Your profile has been updated"))
            return redirect('home')
        return render(request, 'update_user.html', {'update_form':update_form})
 
    else:
        messages.success(request, ("Oops seems like you need to log in to get to that page!"))
        return redirect('login')
    
    
def update_info(request):  
    if request.user.is_authenticated:
        # billing current user
        current_user = Profile.objects.get(user__id=request.user.id)
        # shipping current user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = forms.ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, ("Your profile has been updated"))
            return redirect('update_info')
        return render(request, 'update_info.html', {'form':form, 'shipping_form':shipping_form})

    else:
        messages.success(request, ("Oops seems like you need to log in to get to that page!"))
        return redirect('login')  
    
    
   
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # did they filled the form?
        if request.method == "POST":
            password_form = ChangePasswordForm(current_user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, ("Your password has been updated"))
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(password_form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
            
        else:
            password_form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html',{'password_form':password_form})   
        
        
    messages.success(request, ("Oops seems like you need to log in to get to that page!"))
    return redirect('home')




def product(request, pk):
    product = Proudct.objects.get(id=pk)
    
    return render(request, 'product.html', {'product':product})


    
    
    
