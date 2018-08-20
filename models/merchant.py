from db import db
import helper


class MerchantModel(db.Model):
    __tablename__ = 'merchant'
    code=db.Column(db.String(20),primary_key=True)
    name =db.Column(db.String(80))
    address=db.Column(db.String(100))
    phone=db.Column(db.String(30))
    website =db.Column(db.String(80))
    image =db.Column(db.LargeBinary)
    
    def __init__(self,code,\
                 name,\
                 address,\
                 phone,\
                 website):
        self.code=code
        self.name=name
        self.address=address
        self.phone=phone       
     
    @classmethod
    def find_by_name(cls,merchant_code):
        result = cls.query.filter_by(code=merchant_code).first()
        return result
    
class MerchantImageModel(db.Model):
    __tablename__ = 'merchant'
    __table_args__ = {'extend_existing': True}
    code=db.Column(db.String(20),primary_key=True)
    image =db.Column(db.LargeBinary)
    
    def __init__(self,code,image):
        self.code=code
        self.image=image        

    def getImage(self):
        return self.image
    
    def setImage(self,imageData):
        self.image=imageData
        
    @classmethod
    def find_by_name(cls,merchant_code):
        result = cls.query.filter_by(code=merchant_code).first()
        return result