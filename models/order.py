from db import db
from models.user import UserModel
import helper


class OrderModel(db.Model):
    __tablename__ = 'orders'
    id=db.Column(db.Integer,primary_key=True)
    order_datetime =db.Column(db.DateTime)
    delivery_datetime =db.Column(db.DateTime)
    status =db.Column(db.String(10))
    is_paid =db.Column(db.Boolean)
    payment_type =db.Column(db.String(20))
    by_user_id =db.Column(db.Integer)
    branch_id =db.Column(db.Integer)
    remark=db.Column(db.String(200))
    merchant_code=db.Column(db.String(20))

    def __init__(self,merchant_code,\
                 order_datetime,\
                 delivery_datetime,\
                 status,\
                 is_paid,\
                 payment_type,\
                 by_user_id,\
                 branch_id,\
                 remark):
        self.merchant_code=merchant_code
        self.order_datetime=order_datetime
        self.delivery_datetime=delivery_datetime
        self.status=status
        self.is_paid=is_paid
        self.payment_type=payment_type
        self.by_user_id=by_user_id
        self.branch_id=branch_id
        self.remark=remark
    
    @classmethod
    def find_by_id(cls,merchant_code,id):
        result = cls.query.filter_by(merchant_code=merchant_code).\
        filter_by(id=id).first()
        return result

    @classmethod
    def find_orders(cls,merchant_code,\
                      username,\
                      order_time_since,\
                      order_time_until,\
                      delivery_time_since,\
                      delivery_time_until,\
                      status,\
                      is_paid,\
                      payment_type,\
                      branch_id):
        result = cls.query.filter_by(merchant_code=merchant_code)
        if len(order_time_since)>0:
            result=result.filter(cls.order_datetime >= helper.valid_datetime(order_time_since))
        if len(order_time_until)>0:
            result=result.filter(cls.order_datetime <= helper.valid_datetime(order_time_until))
        if len(delivery_time_since)>0:
            result=result.filter(cls.delivery_datetime >= helper.valid_datetime(delivery_time_since))
        if len(delivery_time_until)>0:
            result=result.filter(cls.delivery_datetime <= helper.valid_datetime(delivery_time_until))
        if len(status)>0:
            result=result.filter_by(status=status)
        if len(is_paid)>0:
            result=result.filter_by(is_paid=is_paid)
        if len(payment_type)>0:
            result=result.filter_by(payment_type=payment_type)
        if len(username)>0:
            try:
                userid=UserModel.name_to_id(merchant_code,username)
                result=result.filter_by(by_user_id=userid)
            except:
                return None
        if len(branch_id)>0:
            result=result.filter_by(branch_id=branch_id)
        return result

