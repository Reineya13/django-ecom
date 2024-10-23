from store.models import Proudct, Profile
import json


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
    #    get the user session key if it exists 
        cart = self.session.get('session_key')
        
    #   if the key doesnt wexits create one
    
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
    #  make sure cart is avilable in every page
    
        self.cart = cart
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)
        if product_id in self.cart:
           
            self.cart[product_id] = self.cart[product_id] + product_qty
            self.session.modified = True
        else:
            # self.cart[product_id] = {'price': str(product_id)}
            self.cart[product_id] =  quantity
            self.session.modified = True
            
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            change_cart = str(self.cart)
            change_cart = change_cart.replace("\'","\"")
            current_user.update(old_cart=str(change_cart))
            
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product_id)}
            self.cart[product_id] =  str(quantity)
            self.session.modified = True
            
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            change_cart = str(self.cart)
            change_cart = change_cart.replace("\'","\"")
            
            
            current_user.update(old_cart=str(change_cart))
        
        
            
            
    def __len__ (self):
        return len(self.cart)  
    
    
    def get_prods(self):
        #get the id of the products
        product_ids = self.cart.keys()
        # get the data of product from DB
        products = Proudct.objects.filter(id__in = product_ids)
        
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        
        ourcart = self.cart
        ourcart[product_id] = product_qty
        
        self.session.modified = True
        thing = self.cart
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            change_cart = str(self.cart)
            change_cart = change_cart.replace("\'","\"")
            
            current_user.update(old_cart=str(change_cart))
        
        return thing
    
    def delete(self, product):
        product_id = str(product)  
        
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            change_cart = str(self.cart)
            change_cart = change_cart.replace("\'","\"")
            
            current_user.update(old_cart=str(change_cart))
        
    def cart_total(self):
        product_ids = self.cart.keys()
        products = Proudct.objects.filter(id__in = product_ids)
        qtys = self.cart
        # start total from 0
        total = 0 
        
        for key, value in qtys.items():
            # int so i can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += (product.sale_price * int(value))
                    else:
                         total += (product.price * int(value))
        return total
    
    def cart_qty_price(self):
        product_ids = self.cart.keys()
        products = Proudct.objects.filter(id__in = product_ids)
        qtys = self.cart
        
        
                
                        
        
        
        
    
    
        
        

           
           
