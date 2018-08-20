from db import db
from sqlalchemy import text
import helper


class UserModel(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    username =db.Column(db.String(20))
    merchant_code=db.Column(db.String(20))
    password=db.Column(db.String(20))
    firstname =db.Column(db.String(80))
    lastname =db.Column(db.String(80))
    status =db.Column(db.String(10))
    user_open_date =db.Column(db.DateTime)
    user_type =db.Column(db.Integer)
    country =db.Column(db.String(50))
    state =db.Column(db.String(50))
    city =db.Column(db.String(50))
    email =db.Column(db.String(80))
    phone =db.Column(db.String(30))
    wechat =db.Column(db.String(50))
    

    def __init__(self,username,\
                 merchant_code,\
                 password,\
                 firstname,\
                 lastname,\
                 status,\
                 user_open_date,\
                 user_type,\
                 country,\
                 state,\
                 city,\
                 email,\
                 phone,\
                 wechat):
        self.username=username
        self.merchant_code=merchant_code
        self.password=password
        self.firstname=firstname
        self.lastname=lastname
        self.status=status
        self.user_open_date=user_open_date
        self.user_type=user_type
        self.country=country
        self.state=state
        self.city=city
        self.email=email
        self.phone=phone
        self.wechat=wechat
    
    @classmethod
    def find_by_name(cls,username,merchant_code):
        result = cls.query.filter_by(merchant_code=merchant_code).\
        filter_by(username=username).first()
        return result

    @classmethod
    def name_to_id(cls,merchant_code,name):
        user = cls.find_by_name(name,merchant_code)
        return user.id
    
    @classmethod
    def id_to_name(cls,merchant_code,_id):
        user = cls.query.filter_by(merchant_code=merchant_code).filter_by(id=_id).first()
        return user.username

    @classmethod
    def find_users(cls,merchant_code,\
                       username,\
                       firstname,\
                       lastname,\
                       user_open_since,\
                       user_open_until,\
                       country,\
                       state,\
                       city,\
                       email,\
                       phone,\
                       wechat):
        result = cls.query.filter_by(merchant_code=merchant_code)
        if len(username)>0:
            result=result.filter(text('username ~ :reg')).params(reg=username)
        if len(firstname)>0:
            result=result.filter(text('firstname ~ :reg')).params(reg=firstname)
        if len(lastname)>0:
            result=result.filter(text('lastname ~ :reg')).params(reg=lastname)
        if len(user_open_since)>0:
            result=result.filter(cls.user_open_date >= helper.valid_date(user_open_since) )
        if len(user_open_until)>0:
            result=result.filter(cls.user_open_date <= helper.valid_date(user_open_until) )
        if len(country)>0:
            result=result.filter(text('country ~ :reg')).params(reg=country)
        if len(state)>0:
            result=result.filter(text('state ~ :reg')).params(reg=state)
        if len(city)>0:
            result=result.filter(text('city ~ :reg')).params(reg=city)
        if len(email)>0:
            result=result.filter_by(email=email)
        if len(phone)>0:
            result=result.filter(text('phone ~ :reg')).params(reg=phone)
        if len(wechat)>0:
            result=result.filter(text('wechat ~ :reg')).params(reg=wechat)
        return result
    
    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
