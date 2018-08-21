from db import db

class AuditModel(db.Model):
    __tablename__ = 'audit'
    id=db.Column(db.Integer,primary_key=True)
    merchant_code =db.Column(db.String(20))
    username=db.Column(db.String(20))
    action=db.Column(db.String(20))
    table_name=db.Column(db.String(50))
    log_datetime=db.Column(db.DateTime)
    log_content=db.Column(db.String(1000))    

    def __init__(self,merchant_code,\
                 username,\
                 action,\
                 table_name,\
                 log_datetime,\
                 log_content):
        self.merchant_code=merchant_code
        self.username=username
        self.action=action
        self.table_name=table_name
        self.log_datetime=log_datetime
        self.log_content=log_content
    