from db import db
from sqlalchemy import text
import helper


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    description=db.Column(db.String(200))
    rate=db.Column(db.Integer)
    c_datetime=db.Column(db.DateTime)
    merchant_code =db.Column(db.String(20))    

    def __init__(self,merchant_code,\
                 description,\
                 rate,\
                 user_id,\
                 c_datetime):
        self.user_id=user_id
        self.description=description
        self.rate=rate
        self.c_datetime=c_datetime
        self.merchant_code=merchant_code
    
    @classmethod
    def find_by_id(cls,merchant_code,id):
        result = cls.query.filter_by(merchant_code=merchant_code).\
        filter_by(id=id).first()
        return result    

    @classmethod
    def find_comments(cls,merchant_code,c_datetime_since,c_datetime_until):
        result = cls.query.filter_by(merchant_code=merchant_code)
        if len(c_datetime_since)>0:
            result=result.filter(cls.c_datetime >= helper.valid_datetime(c_datetime_since))
        if len(c_datetime_until)>0:
            result=result.filter(cls.c_datetime <= helper.valid_datetime(c_datetime_until))
        return result
