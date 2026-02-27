
from fastapi import FastAPI
from models import Product

app=FastAPI()

@app.get("/")
def greet():
    return "Hello, World!"
Products=[
    Product(id=1,name="Laptop",description="A high-performance laptop",price=999.99,quantity=10),
    Product(id=2,name="Smartphone",description="A latest model smartphone",price=   499.99,quantity=20),
    Product(id=3,name="Headphones",description="Noise-cancelling headphones",price=199.99,quantity=15)
]

@app.get("/products")
def get_products():
    return Products

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in Products:
        if product.id == product_id:
            return product
    return {"message": "Product not found"}

@app.post("/products")
def create_product(product: Product):
    Products.append(product)
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for index, product in enumerate(Products):
        if product.id == product_id:
            Products[index] = updated_product
            return updated_product
    return {"message": "Product not found"}


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(Products):
        if product.id == product_id:
            del Products[index]
            return {"message": "Product deleted"}
    return {"message": "Product not found"} 