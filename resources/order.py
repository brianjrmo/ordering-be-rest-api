from datetime import datetime
from flask import request
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required,current_identity
from models.order import OrderModel
from models.user import UserModel
import helper
import security

class Order(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('delivery_datetime',type=helper.valid_datetime,required=False)
    parser.add_argument('status',type=str,required=False)
    parser.add_argument('is_paid',type=bool,required=False)
    parser.add_argument('payment_type',type=str,required=False)
    parser.add_argument('by_user_id',type=int,required=False)
    parser.add_argument('branch_id',type=int,required=False)
    parser.add_argument('remark',type=str,required=False)
    
    @jwt_required()
    def get(self,merchant_code,id):
        order=OrderModel.find_by_id(merchant_code,id)
        if order:
            username=UserModel.id_to_name(merchant_code,order.by_user_id) 
            if security.isAuthorized(merchant_code,username):
                return helper.json(order)
            else:
                return {'message': 'Unauthorized'},401    
        else:
            return {'message': 'Order not found'},404
        
    @jwt_required()
    def post(self,merchant_code,id):
        order=OrderModel.find_by_id(merchant_code,id)
        if order:
            username=UserModel.id_to_name(merchant_code,order.by_user_id)
            if security.isAuthorized(merchant_code,username):
                data=Order.parser.parse_args()
                order.delivery_datetime=helper.selectFirst(data['delivery_datetime'],order.delivery_datetime)
                order.status=helper.selectFirst(data['status'],order.status)
                order.is_paid=helper.selectFirst(data['is_paid'],order.is_paid)
                order.payment_type=helper.selectFirst(data['payment_type'],order.payment_type)
                order.remark=helper.selectFirst(data['remark'],order.remark)
                try:
                    helper.save_to_db(order)
                    return helper.json(order),200
                except Exception as e:
                    return {'message':str(e).split('\n')[0]},500
            else:
                return {'message': 'Unauthorized'},401
        else:
            return {'message': 'Order not found'},404

    @jwt_required()
    def put(self,merchant_code,id):   
        if security.isCorrectMerchant(merchant_code):          
            data=Order.parser.parse_args()
            data['order_datetime']=datetime.now()
            data['by_user_id']=current_identity.id
            order = OrderModel(merchant_code,**data)
            try:
                helper.save_to_db(order)
            except Exception as e:
                return {'message':str(e).split('\n')[0]},500
            return helper.json(order),201
        else:
            return {'message': 'Unauthorized'},401

class OrderList(Resource):
    @jwt_required()
    def get(self,merchant_code):
        if security.isStaff(merchant_code):
            order_time_since=request.args.get('order_time_since')
            order_time_until=request.args.get('order_time_until')
            delivery_time_since=request.args.get('delivery_time_since')
            delivery_time_until=request.args.get('delivery_time_until')
            status=request.args.get('status')
            is_paid = request.args.get('is_paid')
            payment_type = request.args.get('payment_type')
            username = request.args.get('username')
            branch_id = request.args.get('branch_id')
            orderlist=OrderModel.find_orders(merchant_code,\
                                          username,\
                                          order_time_since,\
                                          order_time_until,\
                                          delivery_time_since,\
                                          delivery_time_until,\
                                          status,\
                                          is_paid,\
                                          payment_type,\
                                          branch_id)
            if (orderlist and
                orderlist.count()>0):
                return {x.id:helper.json(x) for x in orderlist}
            else:
                return {'message': 'Order not found'},404
        else:
            return {'message': 'Unauthorized'},401
