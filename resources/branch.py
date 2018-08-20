from datetime import datetime
from flask import request
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.branch import BranchModel
import helper
import security

class Branch(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('branch_name',type=str,required=False)
    parser.add_argument('branch_address',type=str,required=False)
    parser.add_argument('phone',type=str,required=False)
    
    def get(self,merchant_code,id):
        branch=BranchModel.find_by_id(merchant_code,id)
        if branch:
            return helper.json(branch)
        else:
            return {'message': 'Branch not found'},404
        
    @jwt_required()
    def post(self,merchant_code,id):
        if security.isAdmin(merchant_code):
            data=Branch.parser.parse_args()
            branch=BranchModel.find_by_id(merchant_code,id)
            if branch is None:
                return {'message': 'User not found'},404
            else:
                branch.branch_name=helper.selectFirst(data['branch_name'],branch.branch_name)
                branch.branch_address=helper.selectFirst(data['branch_address'],branch.branch_address)
                branch.phone=helper.selectFirst(data['phone'],branch.phone)
                try:
                    helper.save_to_db(branch)
                    return helper.json(branch),200
                except Exception as e:
                    return {'message':str(e).split('\n')[0]},500
            return helper.json(branch),201
        else:
            return {'message': 'Unauthorized'},401

    @jwt_required()
    def put(self,merchant_code,id):
            
        if security.isAdmin(merchant_code):
            data=Branch.parser.parse_args()
            name=data['branch_name']
            if BranchModel.find_by_name(merchant_code,name):
                return {'message':"A branch with name '{}' already exists.".format(name)},400
            branch = BranchModel(merchant_code,**data)
            try:
                helper.save_to_db(branch)
            except Exception as e:
                return {'message':str(e).split('\n')[0]},500
            return helper.json(branch),201
        else:
            return {'message': 'Unauthorized'},401
    
    @jwt_required()
    def delete(self,merchant_code,id):
        if security.isAdmin(merchant_code):
            branch=BranchModel.find_by_id(merchant_code,id)
            if branch:
                helper.delete_from_db(branch)
                return {'message':'branch deleted'}
            else:
                return {'message':'branch not found'}, 400
        else:
            return {'message': 'Unauthorized'},401

class BranchList(Resource):
    def get(self,merchant_code):
        branch_name = request.args.get('branch_name')
        branch_address = request.args.get('branch_address')
        phone = request.args.get('phone')
        branchlist=BranchModel.find_branches(branch_name,\
                                      branch_address,\
                                      phone,\
                                      merchant_code)
        if (branchlist and
            branchlist.count()>0):
            return {x.branch_name:helper.json(x) for x in branchlist}
        else:
            return {'message': 'Branch not found'},404
