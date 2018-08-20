from db import db
from sqlalchemy import text
import helper


class ProductModel(db.Model):
    __tablename__ = 'product'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80))
    update_date=db.Column(db.DateTime)
    status=db.Column(db.String(10))
    category=db.Column(db.String(20))
    quantity=db.Column(db.Integer)
    description=db.Column(db.String(80))
    price=db.Column(db.Float)
    currency=db.Column(db.String(3))
    merchant_code=db.Column(db.String(20))
    image=db.Column(db.LargeBinary)

    def __init__(self,merchant_code,\
                 name,\
                 id,\
                 status,\
                 category,\
                 quantity,\
                 description,\
                 price,\
                 currency,\
                 update_date):

        self.name=name
        self.merchant_code=merchant_code
        self.update_date=update_date
        self.status=status
        self.category=category
        self.quantity=quantity
        self.description=description
        self.price=price
        self.currency=currency
        self.merchant_code=merchant_code        


    @classmethod
    def find_products(cls,name,\
                      category,\
                      description,\
                      merchant_code):
        result = cls.query.filter_by(merchant_code=merchant_code)
        if len(name)>0:
            result=result.filter(text('name ~ :reg')).params(reg=name)
        if len(category)>0:
            result=result.filter(text('category ~ :reg')).params(reg=category)
        if len(description)>0:
            result=result.filter(text('description ~ :reg')).params(reg=description)
        return result
    
    @classmethod
    def find_by_id(cls,merchant_code,_id):
        result = cls.query.filter_by(merchant_code=merchant_code).\
            filter_by(id=_id).first()
        return result
    
    @classmethod
    def find_by_name(cls,merchant_code,name):
        result = cls.query.filter_by(merchant_code=merchant_code).\
            filter_by(name=name).first()
        return result

class ProductImageModel(db.Model):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}
    merchant_code=db.Column(db.String(20))
    id=db.Column(db.Integer,primary_key=True)
    image =db.Column(db.LargeBinary)  

    def getImage(self):
        return self.image
    
    def setImage(self,imageData):
        self.image=imageData
        
    @classmethod
    def find_by_id(cls,merchant_code,id):
        result = cls.query.filter_by(merchant_code=merchant_code).filter_by(id=id).first()
        return result
