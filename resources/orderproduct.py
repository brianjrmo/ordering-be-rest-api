from datetime import datetime
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.orderproduct import OrderProductModel
from models.order import OrderModel
from models.user import UserModel
import helper
import security

class OrderProduct(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('order_id',type=int,required=False)
    parser.add_argument('product_id',type=int,required=False)
    parser.add_argument('quantity',type=int,required=False)
    parser.add_argument('special_price',type=float,required=False)
    parser.add_argument('discount',type=float,required=False)
    parser.add_argument('status',type=str,required=False)
    
        
    @jwt_required()
    def post(self,merchant_code,id):
        orderProduct=OrderProductModel.find_by_id(merchant_code,id)
        if orderProduct:
            order=OrderModel.find_by_id(merchant_code,orderProduct.order_id)
            username=UserModel.id_to_name(merchant_code,order.by_user_id)
            if security.isAuthorized(merchant_code,username):
                data=OrderProduct.parser.parse_args()
                orderProduct.quantity=\
                    helper.selectFirst(data['quantity'],orderProduct.quantity)
                orderProduct.special_price=\
                    helper.selectFirst(data['special_price'],orderProduct.special_price)
                orderProduct.discount=\
                    helper.selectFirst(data['discount'],orderProduct.discount)
                orderProduct.status=\
                    helper.selectFirst(data['status'],orderProduct.status)
                try:
                    helper.save_to_db(orderProduct)
                    return helper.json(orderProduct),200
                except Exception as e:
                        return {'message':str(e).split('\n')[0]},500
            else:
                return {'message': 'Unauthorized'},401
        else:
            return {'message': 'Product not found in order'},404

    @jwt_required()
    def put(self,merchant_code,id):
        data=OrderProduct.parser.parse_args()
        order=OrderModel.find_by_id(merchant_code,data['order_id'])
        if order:
            username=UserModel.id_to_name(merchant_code,order.by_user_id)
            if security.isAuthorized(merchant_code,username):
                data=OrderProduct.parser.parse_args()
                data['order_datetime']=datetime.now()
                orderProduct = OrderProductModel(merchant_code,**data)
                try:
                    helper.save_to_db(orderProduct)
                    return helper.json(orderProduct),200
                except Exception as e:
                    return {'message':str(e).split('\n')[0]},500
            else:
                return {'message': 'Unauthorized'},401
        else:
            return {'message': 'Order ID not found'},404
    
    @jwt_required()
    def delete(self,merchant_code,id):
        orderProduct=OrderProductModel.find_by_id(merchant_code,id)
        if orderProduct:
            order=OrderModel.find_by_id(merchant_code,orderProduct.order_id)
            username=UserModel.id_to_name(merchant_code,order.by_user_id)
            if security.isAuthorized(merchant_code,username):
                try:
                    helper.delete_from_db(orderProduct)
                    return {'message':'Product deleted from order'}, 200
                except Exception as e:
                    return {'message':str(e).split('\n')[0]},500  
            else:
                return {'message': 'Unauthorized'},401  
        else:
            return {'message': 'Product not found in order'},404

class OrderProductList(Resource):
    @jwt_required()
    def get(self,merchant_code,order_id):
        order=OrderModel.find_by_id(merchant_code,order_id)
        if order:
            username=UserModel.id_to_name(merchant_code,order.by_user_id)
            if security.isAuthorized(merchant_code,username):
                orderProdList=OrderProductModel.find_items(merchant_code,order_id)
                if (orderProdList and
                    orderProdList.count()>0):
                    return {x.id:helper.json(x) for x in orderProdList}
                else:
                    return {'message': 'No product in order'},404
            else:
                return {'message': 'Unauthorized'},401
        else:
            return {'message': 'Order not found'},404