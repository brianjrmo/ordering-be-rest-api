from datetime import datetime
from flask import request,send_file
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from io import BytesIO
from models.product import ProductModel,ProductImageModel
import helper
import security

class Product(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('merchant_code',type=str,required=False)
    parser.add_argument('id',type=int,required=False)
    parser.add_argument('name',type=str,required=False)
    parser.add_argument('status',type=str,required=False)
    parser.add_argument('category',type=str,required=False)
    parser.add_argument('quantity',type=int,required=False)
    parser.add_argument('description',type=str,required=False)
    parser.add_argument('price',type=float,required=False)
    parser.add_argument('currency',type=str,required=False)

    def get(self,merchant_code,id):
        product=ProductModel.find_by_id(merchant_code,id)

        if product:
            return helper.json(product),200
        else:
            return {'message': 'Product not found'},404
        
    @jwt_required()
    def post(self,merchant_code,id):
        if security.isAdmin(merchant_code):
            data=Product.parser.parse_args()
            product=ProductModel.find_by_id(merchant_code,id)
            if product is None:
                return {'message': 'Product not found'},404
            else:
                product.name=helper.selectFirst(data['name'],product.name)
                product.update_date=datetime.now()
                product.status=helper.selectFirst(data['status'],product.status)
                product.category=helper.selectFirst(data['category'],product.category)
                product.quantity=helper.selectFirst(data['quantity'],product.quantity)
                product.description=helper.selectFirst(data['description'],product.description)
                product.price=helper.selectFirst(data['price'],product.price)
                product.currency=helper.selectFirst(data['currency'],product.currency)
                try:
                    helper.save_to_db(product)
                    return helper.json(product),200
                except Exception as e:
                    return {'message':str(e).split('\n')[0]},500
        else:
            return {'message': 'Unauthorized'},401

    @jwt_required()
    def put(self,merchant_code,id):
            
        if security.isAdmin(merchant_code):
            data=Product.parser.parse_args()
            name=data['name']
            if ProductModel.find_by_name(merchant_code,name):
                return {'message':"A product with name '{}' already exists.".format(name)},400
            
            data['merchant_code']=merchant_code
            data['update_date']=datetime.now()
            product = ProductModel(**data)
            try:
                helper.save_to_db(product)
            except Exception as e:
                return {'message':str(e).split('\n')[0]},500
            return helper.json(product),201
        else:
            return {'message': 'Unauthorized'},401
    
    @jwt_required()
    def delete(self,merchant_code,id):
        if security.isAdmin(merchant_code):
            product=ProductModel.find_by_id(merchant_code,id)
            if product:
                helper.delete_from_db(product)
                return {'message':'product deleted'}
            else:
                return {'message':'product not found'},400
        else:
            return {'message': 'Unauthorized'},401

class ProductList(Resource):
    def get(self,merchant_code):
        name = request.args.get('name')
        category = request.args.get('category')
        description = request.args.get('description')
        productlist=ProductModel.find_products(name,\
                                      category,\
                                      description,\
                                      merchant_code)
        if (productlist and
            productlist.count()>0):
            return {x.name:helper.json(x) for x in productlist}
        else:
            return {'message': 'Product not found'},404

class ProductImage(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('product_name',type=str,required=False)
    def get(self,merchant_code,id):
        product=ProductImageModel.find_by_id(merchant_code,id)
        if product is None:
            return {'message': 'Product not found'},404
        else:
            imageData=product.getImage()
            filename=product.name.replace(' ','')
            return send_file(BytesIO(imageData),attachment_filename=filename+'.jpg')
        #,as_attachment=True)
        
    @jwt_required()
    def post(self,merchant_code,id):
        if security.isAdmin(merchant_code):
            product=ProductImageModel.find_by_id(merchant_code,id)
            if product is None:
                return {'message': 'Product not found'},404
            else:
                file=request.files['inputfile']
                imageData=file.read();
                if len(imageData) <= helper.imageSizeLimit():
                    product.setImage(imageData)
                    helper.save_to_db(product)
                    return {'message': 'Image uploaded'},200
                else:
                    return {'message': ' over '+str(helper.imageSizeLimit())+' bytes'},413
        else:
            return {'message': 'Unauthorized'},401
#        

