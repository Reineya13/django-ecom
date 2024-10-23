from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Proudct
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    cart_quantites = cart.get_quants
    totals = cart.cart_total()
    
    
    return render(request, 'cart_summary.html',{'cart_products': cart_products , 'cart_quantites' : cart_quantites, 'totals': totals})


def cart_add(request):
    # get the cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
    # get data
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
    # look if exists
        product = get_object_or_404(Proudct, id=product_id)
        
        
        is_sale = product.is_sale
        product_name = product.name
        product_price = product.price
        
        
        
        
    # save to session
        cart.add(product=product, quantity=product_qty)
        
        updated_quantity = cart.cart[str(product_id)]        
        
        if is_sale:
            total_product_price = product.sale_price * int(updated_quantity)
        else:
            total_product_price = product.price * int(updated_quantity) 
        
        cart_total = cart.cart_total()      
        
        
    # send response
        # response = JsonResponse({'Product Name ': product.name})
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity,'is_sale': is_sale, 'cart_total': cart_total, 'sale_price': product.sale_price, 'product_qty':updated_quantity, 'total_product_price': total_product_price,'product_id': product_id, 'product_image': product.image.url,  'product_name':product_name, 'product_price':product_price}) 
        return response
    
    
    
   

def cart_delete(request):
   cart = Cart(request)
   
   if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        
        cart_quantities = cart.get_quants()
        cart_total = cart.cart_total()
        cart_length = cart.__len__()
        print(cart_length)
    
        response = JsonResponse({'product_id': product_id, 'cart_total':cart_total, 'cart_quant': cart_quantities, 'cart_length': cart_length}) 
        return response
    
    

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty')) 
        
        
        cart.update(product=product_id, quantity=product_qty)
    
        response = JsonResponse({'product_qty': product_qty, 'cart_qty': cart.__len__(), 'cart_total': cart.cart_total()})
        return response
    
    
    
    