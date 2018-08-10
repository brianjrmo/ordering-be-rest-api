from db import db
from sqlalchemy import text


class UserModel(db.Model):
#    __tablename__='users'
#    __table_args__ = ({"schema": 'headquater'})
    id=db.Column(db.Integer,primary_key=True)
    username =db.Column(db.String(80))
    password=db.Column(db.String(80))

    def __init__(self,username,schema):
        self.username=username
        self.schema=schema

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def json(self):
        return {'username': self.username, 'password': self.password}

    @classmethod
    def find_by_name(cls,username,schema):
#        return cls.query.filter_by(username=username).first()
        sqlStmt="SELECT * FROM "+ schema +".users where username=:name"
        result = db.session.query(cls).from_statement(text(sqlStmt)).params(name=username).first()
        return result
    
    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
