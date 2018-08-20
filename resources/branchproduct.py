from flask import request
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.branchproduct import BranchProductModel
import helper
import security

class BranchProduct(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('branch_id',type=int,required=False)
    parser.add_argument('product_id',type=int,required=False)
    
    @jwt_required()
    def put(self,merchant_code,id):
        if security.isCorrectMerchant(merchant_code):
            data=BranchProduct.parser.parse_args()
            bp=BranchProductModel.find_by_bp_id(merchant_code,\
                                             data['branch_id'],\
                                             data['product_id'])
            if bp:
                return {'message': 'Product found existed in branch'},400
            else:
                branchproduct = BranchProductModel(merchant_code,**data)
                try:
                    helper.save_to_db(branchproduct)
                    return helper.json(branchproduct),200
                except Exception as e:
                    return {'message':str(e).split('\n')[0]},500
        else:
            return {'message': 'Unauthorized'},401
    
    @jwt_required()
    def delete(self,merchant_code,id):
        branchproduct=BranchProductModel.find_by_id(merchant_code,id)
        if branchproduct:
            if security.isCorrectMerchant(merchant_code):
                try:
                    helper.delete_from_db(branchproduct)
                    return {'message':'Comment deleted'}, 200
                except Exception as e:
                    return {'message':str(e).split('\n')[0]},500  
            else:
                return {'message': 'Unauthorized'},401  
        else:
            return {'message': 'Product not found in branch'},400

class BranchProductList(Resource):
    def get(self,merchant_code):
        branch_id=request.args.get('branch_id')
        branchproduct=BranchProductModel.find_branchproduct(merchant_code,branch_id)
        if (branchproduct and
            branchproduct.count()>0):
            return {x.id:helper.json(x) for x in branchproduct}
        else:
            return {'message': 'Comment not found'},400
