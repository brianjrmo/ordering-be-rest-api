from db import db
from sqlalchemy import text
import helper


class BranchProductModel(db.Model):
    __tablename__ = 'branchproduct'
    id=db.Column(db.Integer,primary_key=True)
    branch_id=db.Column(db.Integer)
    product_id=db.Column(db.Integer)
    merchant_code =db.Column(db.String(20))    

    def __init__(self,merchant_code,\
                 branch_id,\
                 product_id):
        self.branch_id=branch_id
        self.product_id=product_id
        self.merchant_code=merchant_code
    
    @classmethod
    def find_by_bp_id(cls,merchant_code,branch_id,product_id):
        result = cls.query.filter_by(merchant_code=merchant_code).\
            filter_by(branch_id=branch_id).\
            filter_by(product_id=product_id).first()
        return result      

    @classmethod
    def find_by_id(cls,merchant_code,id):
        result = cls.query.filter_by(merchant_code=merchant_code).\
            filter_by(id=id).first()
        return result    

    @classmethod
    def find_branchproduct(cls,merchant_code,branch_id):
        result = cls.query.filter_by(merchant_code=merchant_code)
        if len(branch_id)>0:
            result=result.filter_by(branch_id=branch_id)
        return result
