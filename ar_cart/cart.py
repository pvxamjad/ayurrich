
from ar_store.models import ProductRegistration

class Cart():
    def __init__(self,request):
        self.session = request.session

        # get the current session key if it is existed 

        cart = self.session.get('session_key')

        # if the user is new 

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available on all pages of site 
        self.cart = cart



    def add(self, product ,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # logic 
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id] = quantity
        self.session.modified = True
    

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True
        

    def __len__(self):
        return len(self.cart)
    

    def get_prods(self):
        # get ids from cart 
        product_ids = self.cart.keys()
        # use ids to lookup product in db model 
        products = ProductRegistration.objects.filter(id__in=product_ids)
        # return those lookup product 
        return products
    

    def get_quants(self):
        return self.cart
    
    def clear(self):
        # Clear the cart from the session
        self.session['session_key'] = {}
        self.session.modified = True



        