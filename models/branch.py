from db import db
from sqlalchemy import text
import helper


class BranchModel(db.Model):
    __tablename__ = 'branches'
    id=db.Column(db.Integer,primary_key=True)
    branch_name =db.Column(db.String(80))
    branch_address=db.Column(db.String(100))
    phone=db.Column(db.String(30))
    merchant_code =db.Column(db.String(20))    

    def __init__(self,merchant_code,\
                 branch_name,\
                 branch_address,\
                 phone):
        self.branch_name=branch_name
        self.branch_address=branch_address
        self.phone=phone
        self.merchant_code=merchant_code
    
    @classmethod
    def find_by_id(cls,merchant_code,id):
        result = cls.query.filter_by(merchant_code=merchant_code).\
        filter_by(id=id).first()
        return result    

    @classmethod
    def find_by_name(cls,merchant_code,name):
        result = cls.query.filter_by(merchant_code=merchant_code).\
        filter_by(branch_name=name).first()
        return result

    @classmethod
    def find_branches(cls,branch_name,\
                       branch_address,\
                       phone,\
                       merchant_code):
        result = cls.query.filter_by(merchant_code=merchant_code)
        if len(branch_name)>0:
            result=result.filter(text('branch_name ~ :reg')).params(reg=branch_name)
        if len(branch_address)>0:
            result=result.filter(text('branch_address ~ :reg')).params(reg=branch_address)
        if len(phone)>0:
            result=result.filter(text('phone ~ :reg')).params(reg=phone)
        return result

