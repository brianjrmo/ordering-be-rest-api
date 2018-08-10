from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate,identity
from resources.user import UserRegister,UserList
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL',\
              'postgresql://postgres:593935@localhost/urstodr001')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.secret_key='brianmo'
api=Api(app)

#@app.before_first_request
#def create_tables():
#    db.create_all()

jwt = JWT(app,authenticate,identity) #/auth

api.add_resource(UserRegister, '/<string:schema>/user/<string:username>')
api.add_resource(UserList,'/<string:schema>/users')

if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)
