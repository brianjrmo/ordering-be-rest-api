from datetime import datetime
from flask import request
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.user import UserModel
import helper
import security

class UserRegister(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('password',type=str,required=False)
    parser.add_argument('firstname',type=str,required=False)
    parser.add_argument('lastname',type=str,required=False)
    parser.add_argument('status',type=str,required=False)
    parser.add_argument('user_type',type=int,required=False)
    parser.add_argument('country',type=str,required=False)
    parser.add_argument('state',type=str,required=False)
    parser.add_argument('city',type=str,required=False)
    parser.add_argument('email',type=str,required=False)
    parser.add_argument('phone',type=str,required=False)
    parser.add_argument('wechat',type=str,required=False)
    
    @jwt_required()
    def get(self,username,merchant_code):
        if security.isAuthorized(merchant_code,username):
            user=UserModel.find_by_name(username,merchant_code)
            if user:
                return helper.json(user)
            else:
                return {'message': 'User not found'},404
        else:
            return {'message': 'Unauthorized'},401
        
    @jwt_required()
    def post(self,username,merchant_code):
        if security.isAuthorized(merchant_code,username):
            data=UserRegister.parser.parse_args()
            user=UserModel.find_by_name(username,merchant_code)
            if user is None:
                return {'message': 'User not found'},404
            else:
                user.password=helper.selectFirst(data['password'],user.password)
                user.firstname=helper.selectFirst(data['firstname'],user.firstname)
                user.lastname=helper.selectFirst(data['lastname'],user.lastname)
                user.status=helper.selectFirst(data['status'],user.status)
                user.country=helper.selectFirst(data['country'],user.country)
                user.state=helper.selectFirst(data['state'],user.state)
                user.city=helper.selectFirst(data['city'],user.city)
                user.email=helper.selectFirst(data['email'],user.email)
                user.phone=helper.selectFirst(data['phone'],user.phone)
                user.wechat=helper.selectFirst(data['wechat'],user.wechat)
                helper.save_to_db(user)
                return helper.json(user),200
        else:
            return {'message': 'Unauthorized'},401

    @jwt_required()
    def put(self,username,merchant_code):
            
        if security.isCorrectMerchant(merchant_code):
            if UserModel.find_by_name(username,merchant_code):
                return {'message':"A user with name '{}' already exists.".format(username)},400
            
            #all new user by default the lowest level. need to be change by staff after create
            data=UserRegister.parser.parse_args()
            data['user_type']=helper.userTypeTypical()
            data['user_open_date']=datetime.now()
            user = UserModel(username,merchant_code,**data)
            try:
                helper.save_to_db(user)
            except Exception as e:
                return {'message':str(e).split('\n')[0]},500
            return helper.json(user),201
        else:
            return {'message': 'Unauthorized'},401
    
    @jwt_required()
    def delete(self,username,merchant_code):
        if security.isAuthorized(merchant_code,username):
            user=UserModel.find_by_name(username,merchant_code)
            if user:
                helper.delete_from_db(user)
                return {'message':'user deleted'}
            else:
                return {'message':'user not found'}, 400
        else:
            return {'message': 'Unauthorized'},401

class UserList(Resource):
    @jwt_required()
    def get(self,merchant_code):
        if security.isStaff(merchant_code):
            username = request.args.get('username')
            firstname = request.args.get('firstname')
            lastname = request.args.get('lastname')
            user_open_after = request.args.get('user_open_after')
            user_open_before = request.args.get('user_open_before')
            country = request.args.get('country')
            state = request.args.get('state')
            city = request.args.get('city')
            email = request.args.get('email')
            phone = request.args.get('phone')
            wechat = request.args.get('wechat')
            userlist=UserModel.find_users(merchant_code,\
                                          username,\
                                          firstname,\
                                          lastname,\
                                          user_open_after,\
                                          user_open_before,\
                                          country,\
                                          state,\
                                          city,\
                                          email,\
                                          phone,\
                                          wechat)
            if (userlist and
                userlist.count()>0):
                return {x.username:helper.json(x) for x in userlist}
            else:
                return {'message': 'User not found'},404
        else:
            return {'message': 'Unauthorized'},401

class UserType(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('user_type',type=int,required=True)
    @jwt_required()
    def post(self,username,merchant_code):
        if security.isAdmin(merchant_code):
            data=UserType.parser.parse_args()
            user=UserModel.find_by_name(username,merchant_code)
            if user is None:
                return {'message': 'User not found'},404
            else:
                user.user_type=data['user_type']
                helper.save_to_db(user)
                return helper.json(user),200
        else:
            return {'message': 'Unauthorized'},401
#        

