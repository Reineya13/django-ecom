from .cart import Cart

# create cart processors so our cart work in every page

def cart(request):
    # return the default data from the cart
    return {'cart': Cart(request)}

