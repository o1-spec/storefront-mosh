from locust import HttpUser, task,between
from random import randint

class WebsiteUser(HttpUser):
    wait_time = between(1,5)
    #Viewing Products
    @task(2)
    def view_products(self):
        collection_id = randint(2,6)
        self.client.get(f'/store/products/?collection_id={collection_id}',name='/store/products')
    #Viewing product details
    @task(4) #Twice more likely to be executed than the first one
    def view_product(self):
        product_id = randint(1,1000)
        self.client.get(f'/store/product/{product_id}', name='/store.products/:id')
        
    #Adding Product to cart
    @task(1)
    def add_to_cart(self):
        product_id = randint(1,1000)
        self.client.post(
            f'/store/carts/{self.card_id}/items/',
            name='/store/carts/items',
            json={'product_id':product_id, 'quantity': 1}
        )
    @task 
    def say_hello(self):
        self.client.get('/playground/hello')
        
    def on_start(self):
        response = self.client.post('/store/carts/')
        result = response.json()
        self.card_id = result['id']