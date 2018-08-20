from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate,identity
from resources.user import UserRegister,UserType,UserList
from resources.merchant import Merchant,MerchantImage
from resources.product import Product,ProductList,ProductImage
from resources.branch import Branch,BranchList
from resources.order import Order,OrderList
from resources.orderproduct import OrderProduct,OrderProductList
from resources.comment import Comment,CommentList
from resources.branchproduct import BranchProduct,BranchProductList
import os
import helper

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL',\
              'postgresql://postgres:593935@localhost/urstodr001')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)

app.secret_key='brianmo'
api=Api(app)

#@app.before_first_request
#def create_tables():
#    db.create_all()

jwt = JWT(app,authenticate,identity) #/auth

api.add_resource(Merchant, '/<string:code>')
api.add_resource(MerchantImage, '/<string:code>/image')
api.add_resource(UserRegister, '/<string:merchant_code>/user/<string:username>')
api.add_resource(UserType, '/<string:merchant_code>/usertype/<string:username>')
api.add_resource(UserList, '/<string:merchant_code>/userlist')
api.add_resource(Product, '/<string:merchant_code>/product/<int:id>')
api.add_resource(ProductList, '/<string:merchant_code>/productlist')
api.add_resource(ProductImage, '/<string:merchant_code>/productimage/<int:id>')
api.add_resource(Branch, '/<string:merchant_code>/branch/<int:id>')
api.add_resource(BranchList, '/<string:merchant_code>/branchlist')
api.add_resource(Order, '/<string:merchant_code>/order/<int:id>')
api.add_resource(OrderList, '/<string:merchant_code>/orderlist')
api.add_resource(OrderProduct, '/<string:merchant_code>/orderproduct/<int:id>')
api.add_resource(OrderProductList, '/<string:merchant_code>/orderproductlist/<int:order_id>')
api.add_resource(Comment, '/<string:merchant_code>/comment/<int:id>')
api.add_resource(CommentList, '/<string:merchant_code>/commentlist')
api.add_resource(BranchProduct, '/<string:merchant_code>/branchproduct/<int:id>')
api.add_resource(BranchProductList, '/<string:merchant_code>/branchproductlist')

if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)
