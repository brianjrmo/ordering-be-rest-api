from datetime import datetime
from flask import request
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required,current_identity
from models.comment import CommentModel
import helper
import security

class Comment(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('description',type=str,required=False)
    parser.add_argument('rate',type=int,required=False)
    
        
    @jwt_required()
    def post(self,merchant_code,id):
        comment=CommentModel.find_by_id(merchant_code,id)
        if comment:
            if security.isSelf(merchant_code,comment.user_id):
                data=Comment.parser.parse_args()
                comment.description=helper.selectFirst(data['description'],comment.description)
                comment.rate=helper.selectFirst(data['rate'],comment.rate)
                comment.c_datetime=datetime.now()
                try:
                    helper.save_to_db(comment)
                    return helper.json(comment),200
                except Exception as e:
                        return {'message':str(e).split('\n')[0]},500
            else:
                return {'message': 'Unauthorized'},401
        else:
            return {'message': 'Comment not found'},400
    

    @jwt_required()
    def put(self,merchant_code,id):
        if security.isCorrectMerchant(merchant_code):
            data=Comment.parser.parse_args()
            data['user_id']=current_identity.id
            data['c_datetime']=datetime.now()
            comment = CommentModel(merchant_code,**data)
            try:
                helper.save_to_db(comment)
                return helper.json(comment),200
            except Exception as e:
                return {'message':str(e).split('\n')[0]},500
        else:
            return {'message': 'Unauthorized'},401
    
    @jwt_required()
    def delete(self,merchant_code,id):
        comment=CommentModel.find_by_id(merchant_code,id)
        if comment:
            if security.isSelf(merchant_code,comment.user_id):
                try:
                    helper.delete_from_db(comment)
                    return {'message':'Comment deleted'}, 200
                except Exception as e:
                    return {'message':str(e).split('\n')[0]},500  
            else:
                return {'message': 'Unauthorized'},401  
        else:
            return {'message': 'Comment not found'},400

class CommentList(Resource):
    def get(self,merchant_code):
        comment_time_since=request.args.get('comment_time_since')
        comment_time_until=request.args.get('comment_time_until')
        comment=CommentModel.find_comments(merchant_code,\
                                           comment_time_since,\
                                           comment_time_until)
        if (comment and
            comment.count()>0):
            return {x.id:helper.json(x) for x in comment}
        else:
            return {'message': 'Comment not found'},400
