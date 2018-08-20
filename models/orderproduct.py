from db import db
from sqlalchemy import text
import helper


class OrderProductModel(db.Model):
    __tablename__ = 'orderproduct'
    id=db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.Integer)
    product_id=db.Column(db.Integer)
    quantity=db.Column(db.Integer)
    special_price=db.Column(db.Float)
    discount=db.Column(db.Float)
    order_datetime=db.Column(db.DateTime)
    status=db.Column(db.String(10))
    merchant_code =db.Column(db.String(20))    

    def __init__(self,merchant_code,\
                 order_id,\
                 product_id,\
                 quantity,\
                 special_price,\
                 discount,\
                 status,\
                 order_datetime):
        self.order_id=order_id
        self.product_id=product_id
        self.quantity=quantity
        self.special_price=special_price
        self.discount=discount
        self.order_datetime=order_datetime
        self.status=status
        self.merchant_code=merchant_code
    
    @classmethod
    def find_by_id(cls,merchant_code,id):
        result = cls.query.filter_by(merchant_code=merchant_code).\
        filter_by(id=id).first()
        return result    

    @classmethod
    def find_items(cls,merchant_code,order_id):
        result = cls.query.filter_by(merchant_code=merchant_code).\
                filter_by(order_id=order_id)
        return result
