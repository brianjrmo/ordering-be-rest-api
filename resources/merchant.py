from flask import request,send_file
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from io import BytesIO
from models.merchant import MerchantModel,MerchantImageModel
import helper
import security

class Merchant(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('name',type=str,required=False)
    parser.add_argument('address',type=str,required=False)
    parser.add_argument('phone',type=str,required=False)
    parser.add_argument('website',type=str,required=False)
    
    def get(self,code):
        merchant=MerchantModel.find_by_name(code)
        if merchant:
            return helper.json(merchant)
        else:
            return {'message': 'merchant not found'},404
    
    @jwt_required()
    def post(self,code):
        if security.isAdmin(code):
            data=Merchant.parser.parse_args()
            merchant=MerchantModel.find_by_name(code)
            if merchant is None:
                return {'message': 'Merchant not found'},404
            else:
                merchant.name=helper.selectFirst(data['name'],merchant.name)
                merchant.address=helper.selectFirst(data['address'],merchant.address)
                merchant.phone=helper.selectFirst(data['phone'],merchant.phone)
                merchant.website=helper.selectFirst(data['website'],merchant.website)
                helper.save_to_db(merchant)
                return helper.json(merchant),200
        else:
            return {'message': 'Unauthorized'},401
        
class MerchantImage(Resource):
    def get(self,code):
        merchant=MerchantImageModel.find_by_name(code)
        if merchant is None:
            return {'message': 'Merchant not found'},404
        else:
            imageData=merchant.getImage()
            return send_file(BytesIO(imageData),attachment_filename=code+'.jpg')
        #,as_attachment=True)
        
    @jwt_required()
    def post(self,code):
        if security.isAdmin(code):
            merchant=MerchantImageModel.find_by_name(code)
            if merchant is None:
                return {'message': 'Merchant not found'},404
            else:
                file=request.files['inputfile']
                imageData=file.read();
                if len(imageData) <= helper.imageSizeLimit():
                    merchant.setImage(imageData)
                    helper.save_to_db(merchant)
                    return {'message': 'Image uploaded'},200
                else:
                    return {'message': ' over '+str(helper.imageSizeLimit())+' bytes'},413
        else:
            return {'message': 'Unauthorized'},401