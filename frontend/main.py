
from fastapi import Depends, FastAPI
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session
app=FastAPI()
database_models.Base.metadata.create_all(bind=engine)   

@app.get("/")
def greet():
    return "Hello, World!"
Products=[
    Product(id=1,name="Laptop",description="A high-performance laptop",price=999.99,quantity=10),
    Product(id=2,name="Smartphone",description="A latest model smartphone",price=   499.99,quantity=20),
    Product(id=3,name="Headphones",description="Noise-cancelling headphones",price=199.99,quantity=15)
]

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()
def init_db():
    
    db=session()
    count=db.query(database_models.Product).count()
    if count == 0:

        for product in Products:
             db.add(database_models.Product(**product.model_dump()))
             db.commit()
    

init_db()
    
@app.get("/products")
def get_products(db:Session=Depends(get_db)):
    products=db.query(database_models.Product).all()
    db.close()
    return products

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    db=session()
    product=db.query(Product).filter(Product.id == product_id).first()
    db.close()
    if product:
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